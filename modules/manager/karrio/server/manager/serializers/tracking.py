import typing
import logging
from django.utils import timezone

import karrio.lib as lib
import karrio.server.serializers as serializers
import karrio.server.core.utils as utils
from karrio.server.core.gateway import Shipments, Carriers
from karrio.server.core.serializers import (
    TrackingDetails,
    TrackingRequest,
    ShipmentStatus,
    TrackerStatus,
    TrackingInfo,
)

import karrio.server.manager.models as models

logger = logging.getLogger(__name__)
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

    def create(self, validated_data: dict, context, **kwargs) -> models.Tracking:
        options = validated_data["options"]
        metadata = validated_data["metadata"]
        carrier_filter = validated_data["carrier_filter"]
        tracking_number = validated_data["tracking_number"]
        account_number = validated_data.get("account_number")
        info = validated_data.get("info")
        reference = validated_data.get("reference")
        pending_pickup = validated_data.get("pending_pickup")
        carrier = Carriers.first(
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

        return models.Tracking.objects.create(
            created_by=context.user,
            tracking_number=tracking_number,
            account_number=account_number,
            events=lib.to_dict(response.tracking.events),
            test_mode=response.tracking.test_mode,
            delivered=response.tracking.delivered,
            status=response.tracking.status,
            tracking_carrier=carrier,
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
            carrier = (
                Carriers.first(
                    context=context, **{**DEFAULT_CARRIER_FILTER, **carrier_filter}
                )
                or instance.tracking_carrier
            )

            response = Shipments.track(
                payload=TrackingRequest(
                    dict(tracking_numbers=[instance.tracking_number], options=options)
                ).data,
                carrier=carrier,
            )
            # update values only if changed; This is important for webhooks notification
            changes = []
            details = response.tracking
            info = lib.to_dict(details.info or {})
            events = utils.process_events(
                response_events=details.events, current_events=instance.events
            )

            if events != instance.events:
                instance.events = events
                changes.append("events")

            if response.messages != instance.messages:
                instance.messages = lib.to_dict(response.messages)
                changes.append("messages")

            if details.delivered != instance.delivered:
                instance.delivered = details.delivered
                changes.append("delivered")

            if details.status != instance.status:
                instance.status = details.status
                changes.append("status")

            if details.estimated_delivery != instance.estimated_delivery:
                instance.estimated_delivery = details.estimated_delivery
                changes.append("estimated_delivery")

            if details.options != instance.options:
                instance.options = details.options
                changes.append("options")

            if any(info.keys()) and info != instance.info:
                instance.info = serializers.process_dictionaries_mutations(
                    ["info"], dict(info=info), instance
                )["info"]
                changes.append("info")

            if carrier.id != instance.tracking_carrier.id:
                instance.carrier = carrier
                changes.append("tracking_carrier")

            if details.images is not None and (
                details.images.delivery_image != instance.delivery_image
                or details.images.signature_image != instance.signature_image
            ):
                changes.append("delivery_image")
                changes.append("signature_image")
                instance.delivery_image = (
                    details.images.delivery_image or instance.delivery_image
                )
                instance.signature_image = (
                    details.images.signature_image or instance.signature_image
                )

            if any(changes):
                instance.save(update_fields=changes)
                update_shipment_tracker(instance)

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
        logger.exception("Failed to update the tracked shipment", e)
