import typing
from django.db import transaction
from django.utils import timezone

import karrio.lib as lib
import karrio.server.serializers as serializers
import karrio.server.core.utils as utils
from karrio.server.core.logging import logger
from karrio.server.core.gateway import Shipments, Connections
from karrio.server.core.utils import create_carrier_snapshot, resolve_carrier
from karrio.server.core.serializers import (
    TRACKER_STATUS,
    TrackingDetails,
    TrackingEvent,
    TrackingRequest,
    ShipmentStatus,
    TrackerStatus,
    TrackingInfo,
)

import karrio.server.manager.models as models
DEFAULT_CARRIER_FILTER: typing.Any = dict(active=True, capability="tracking")


@serializers.owned_model_serializer
class TrackingSerializer(TrackingDetails):
    carrier_id = serializers.CharField(required=False)
    carrier_name = serializers.CharField(required=False)
    test_mode = serializers.BooleanField(required=False)
    options = serializers.PlainDictField(
        required=False,
        default={},
        help_text="additional tracking options",
    )
    info = TrackingInfo(
        required=False,
        default={},
        help_text="The package and shipment tracking details",
    )
    metadata = serializers.PlainDictField(
        required=False,
        default={},
        help_text="The carrier user metadata.",
    )

    @transaction.atomic
    def create(self, validated_data: dict, context, **kwargs) -> models.Tracking:
        options = validated_data["options"]
        metadata = validated_data["metadata"]
        carrier_filter = validated_data["carrier_filter"]
        tracking_number = validated_data["tracking_number"]
        account_number = validated_data.get("account_number")
        info = validated_data.get("info")
        reference = validated_data.get("reference")
        pending_pickup = validated_data.get("pending_pickup")
        carrier = Connections.first(
            context=context,
            **{"raise_not_found": True, **DEFAULT_CARRIER_FILTER, **carrier_filter}
        )

        response = Shipments.track(
            TrackingRequest(
                dict(
                    tracking_numbers=[tracking_number],
                    account_number=account_number,
                    reference=reference,
                    options=options,
                    info=info,
                )
            ).data,
            carrier=carrier,
            raise_on_error=(pending_pickup is not True),
        )

        # Apply picked_up transformation for initial events
        events = utils._ensure_picked_up_status(lib.to_dict(response.tracking.events))

        return models.Tracking.objects.create(
            created_by=context.user,
            tracking_number=tracking_number,
            account_number=account_number,
            events=events,
            test_mode=response.tracking.test_mode,
            delivered=response.tracking.delivered,
            status=response.tracking.status,
            carrier=create_carrier_snapshot(carrier),
            estimated_delivery=response.tracking.estimated_delivery,
            messages=lib.to_dict(response.messages),
            info=lib.to_dict(response.tracking.info),
            meta=response.tracking.meta,
            options=response.tracking.options,
            reference=reference,
            metadata=metadata,
            delivery_image=getattr(response.tracking.images, "delivery_image", None),
            signature_image=getattr(response.tracking.images, "signature_image", None),
        )

    @transaction.atomic
    def update(
        self, instance: models.Tracking, validated_data: dict, context, **kwargs
    ) -> models.Tracking:
        last_fetch = (
            timezone.now() - instance.updated_at
        ).seconds / 60  # minutes since last fetch

        if last_fetch >= 1 and instance.delivered is not True:
            carrier_filter = validated_data["carrier_filter"]
            options = {
                instance.tracking_number: {
                    **(instance.options.get(instance.tracking_number) or {}),
                    **(
                        (validated_data.get("options") or {}).get(
                            instance.tracking_number
                        )
                        or {}
                    ),
                }
            }
            # Try to get carrier from filter, fall back to resolved carrier from snapshot
            carrier = Connections.first(
                context=context, **{**DEFAULT_CARRIER_FILTER, **carrier_filter}
            ) or resolve_carrier(instance.carrier, context)

            response = Shipments.track(
                payload=TrackingRequest(
                    dict(tracking_numbers=[instance.tracking_number], options=options)
                ).data,
                carrier=carrier,
            )

            # Handle carrier change separately (not part of tracking_details)
            current_carrier_id = (instance.carrier or {}).get("connection_id")
            if carrier and carrier.id != current_carrier_id:
                instance.carrier = create_carrier_snapshot(carrier)
                instance.save(update_fields=["carrier"])

            # Use update_tracker for the rest of the tracking details
            update_tracker(
                instance,
                dict(
                    events=response.tracking.events,
                    messages=response.messages,
                    delivered=response.tracking.delivered,
                    status=response.tracking.status,
                    estimated_delivery=response.tracking.estimated_delivery,
                    options=response.tracking.options,
                    info=lib.to_dict(response.tracking.info or {}),
                    images=response.tracking.images,
                ),
            )

        return instance


@serializers.owned_model_serializer
class TrackerUpdateData(serializers.Serializer):
    info = TrackingInfo(
        required=False,
        allow_null=True,
        help_text="The package and shipment tracking details",
    )
    metadata = serializers.PlainDictField(
        required=False, help_text="User metadata for the tracker"
    )

    @transaction.atomic
    def update(
        self, instance: models.Tracking, validated_data: dict, **kwargs
    ) -> models.Tracking:
        changes = []
        data = validated_data.copy()

        for key, val in data.items():
            if key in models.Tracking.DIRECT_PROPS and getattr(instance, key) != val:
                setattr(instance, key, val)
                changes.append(key)
                validated_data.pop(key)

        if any(changes):
            instance.save(update_fields=changes)

        return instance


def can_mutate_tracker(
    tracker: models.Tracking,
    update: bool = False,
    payload: dict = None,
):
    if update and tracker.delivered and [*(payload or {}).keys()] == ["metadata"]:
        return

    if update and all([key in ["metadata", "info"] for key in (payload or {}).keys()]):
        return


def update_shipment_tracker(tracker: models.Tracking):
    try:
        if tracker.status == TrackerStatus.delivered.value:
            status = ShipmentStatus.delivered.value
        elif tracker.status == TrackerStatus.pending.value:
            status = tracker.shipment.status
        elif tracker.status == TrackerStatus.picked_up.value:
            status = ShipmentStatus.shipped.value
        elif tracker.status == TrackerStatus.out_for_delivery.value:
            status = ShipmentStatus.out_for_delivery.value
        elif tracker.status == TrackerStatus.delivery_failed.value:
            status = ShipmentStatus.delivery_failed.value
        elif tracker.status in [
            TrackerStatus.on_hold.value,
            TrackerStatus.delivery_delayed.value,
        ]:
            status = ShipmentStatus.needs_attention.value
        else:
            status = ShipmentStatus.in_transit.value

        if tracker.shipment is not None and tracker.shipment.status != status:
            tracker.shipment.status = status
            tracker.shipment.save(update_fields=["status"])
    except Exception as e:
        logger.exception("Failed to update the tracked shipment", error=str(e), tracker_id=tracker.id, tracking_number=tracker.tracking_number)


@transaction.atomic
def update_tracker(tracker: models.Tracking, tracking_details: dict) -> models.Tracking:
    """Update tracker with new tracking details from webhook or external source.

    This utility function consolidates the change detection logic for updating
    a tracker instance. It only saves fields that have changed and triggers
    the shipment status update via update_shipment_tracker.

    Args:
        tracker: The Tracking model instance to update
        tracking_details: Dictionary containing tracking details with keys like:
            - events: List of tracking event dictionaries
            - messages: List of message dictionaries
            - delivered: Boolean delivery status
            - status: Tracker status string
            - estimated_delivery: Estimated delivery date string
            - options: Dictionary of tracking options
            - meta: Dictionary of metadata
            - info: Dictionary of tracking info
            - images: Dictionary with delivery_image and signature_image

    Returns:
        The updated Tracking model instance
    """
    try:
        changes = []

        # Process events - merge with existing events
        new_events = tracking_details.get("events") or []
        if new_events:
            events = utils.process_events(
                response_events=new_events, current_events=tracker.events
            )
            if events != tracker.events:
                tracker.events = events
                changes.append("events")

        # Update messages
        messages = tracking_details.get("messages")
        if messages is not None and messages != tracker.messages:
            tracker.messages = lib.to_dict(messages)
            changes.append("messages")

        # Update delivered status
        delivered = tracking_details.get("delivered")
        if delivered is not None and delivered != tracker.delivered:
            tracker.delivered = delivered
            changes.append("delivered")

        # Update status
        status = tracking_details.get("status")
        if status is not None and status != tracker.status:
            tracker.status = status
            changes.append("status")

        # Update estimated delivery
        estimated_delivery = tracking_details.get("estimated_delivery")
        if estimated_delivery is not None and estimated_delivery != tracker.estimated_delivery:
            tracker.estimated_delivery = estimated_delivery
            changes.append("estimated_delivery")

        # Update options
        options = tracking_details.get("options")
        if options is not None and options != tracker.options:
            tracker.options = options
            changes.append("options")

        # Update meta
        meta = tracking_details.get("meta")
        if meta is not None and meta != tracker.meta:
            tracker.meta = {**(tracker.meta or {}), **meta}
            changes.append("meta")

        # Update info - merge with existing info
        info = tracking_details.get("info") or {}
        if any(info.keys()) and info != tracker.info:
            tracker.info = serializers.process_dictionaries_mutations(
                ["info"], dict(info=info), tracker
            )["info"]
            changes.append("info")

        # Sync estimated_delivery to info.expected_delivery if updated
        if estimated_delivery is not None:
            current_expected = (tracker.info or {}).get("expected_delivery")
            if current_expected != estimated_delivery:
                tracker.info = {**(tracker.info or {}), "expected_delivery": estimated_delivery}
                if "info" not in changes:
                    changes.append("info")

        # Update images
        images = tracking_details.get("images") or {}
        delivery_image = images.get("delivery_image") if isinstance(images, dict) else getattr(images, "delivery_image", None)
        signature_image = images.get("signature_image") if isinstance(images, dict) else getattr(images, "signature_image", None)

        if delivery_image is not None or signature_image is not None:
            if delivery_image != tracker.delivery_image or signature_image != tracker.signature_image:
                if delivery_image is not None:
                    tracker.delivery_image = delivery_image
                    changes.append("delivery_image")
                if signature_image is not None:
                    tracker.signature_image = signature_image
                    changes.append("signature_image")

        # Save changes and update associated shipment
        if any(changes):
            tracker.save(update_fields=changes)
            update_shipment_tracker(tracker)
            logger.info(
                "Tracker updated via webhook",
                tracker_id=tracker.id,
                tracking_number=tracker.tracking_number,
                changes=changes,
            )

        return tracker

    except Exception as e:
        logger.exception(
            "Failed to update tracker",
            error=str(e),
            tracker_id=tracker.id,
            tracking_number=tracker.tracking_number,
        )
        return tracker


class TrackerEventInjectRequest(serializers.Serializer):
    """Request payload for injecting tracking events."""

    events = TrackingEvent(
        many=True,
        required=True,
        help_text="List of tracking events to inject into the tracker",
    )
    status = serializers.ChoiceField(
        required=False,
        allow_null=True,
        choices=TRACKER_STATUS,
        help_text="Optional: Override the tracker status",
    )
    delivered = serializers.BooleanField(
        required=False,
        default=False,
        help_text="Optional: Mark the tracker as delivered",
    )
    estimated_delivery = serializers.DateField(
        required=False,
        allow_null=True,
        help_text="Optional: Set the estimated delivery date",
    )
