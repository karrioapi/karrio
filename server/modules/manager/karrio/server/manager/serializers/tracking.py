import logging
import typing
from django.utils import timezone
from karrio.server.serializers import owned_model_serializer
from rest_framework.serializers import CharField, BooleanField
from karrio.core.utils import DP
from karrio.server.core.gateway import Shipments, Carriers
from karrio.server.core.serializers import (
    TrackingDetails,
    TrackingRequest,
    ShipmentStatus,
    TrackerStatus,
)

import karrio.server.manager.models as models

logger = logging.getLogger(__name__)
DEFAULT_CARRIER_FILTER: typing.Any = dict(active=True, capability="tracking")


@owned_model_serializer
class TrackingSerializer(TrackingDetails):
    carrier_id = CharField(required=False)
    carrier_name = CharField(required=False)
    test_mode = BooleanField(required=False)
    pending = BooleanField(required=False)

    def create(self, validated_data: dict, context, **kwargs) -> models.Tracking:
        carrier_filter = validated_data["carrier_filter"]
        tracking_number = validated_data["tracking_number"]
        carrier = Carriers.first(
            context=context,
            **{"raise_not_found": True, **DEFAULT_CARRIER_FILTER, **carrier_filter}
        )

        response = Shipments.track(
            TrackingRequest(dict(tracking_numbers=[tracking_number])).data,
            carrier=carrier,
            raise_on_error=False,
        )

        return models.Tracking.objects.create(
            created_by=context.user,
            tracking_number=tracking_number,
            events=DP.to_dict(response.tracking.events),
            test_mode=response.tracking.test_mode,
            delivered=response.tracking.delivered,
            status=response.tracking.status,
            tracking_carrier=carrier,
            estimated_delivery=response.tracking.estimated_delivery,
            messages=DP.to_dict(response.messages),
        )

    def update(
        self, instance: models.Tracking, validated_data: dict, context, **kwargs
    ) -> models.Tracking:
        last_fetch = (
            timezone.now() - instance.updated_at
        ).seconds / 60  # minutes since last fetch

        if last_fetch >= 30 and instance.delivered is not True:
            carrier_filter = validated_data["carrier_filter"]
            carrier = (
                Carriers.first(
                    context=context, **{**DEFAULT_CARRIER_FILTER, **carrier_filter}
                )
                or instance.tracking_carrier
            )

            response = Shipments.track(
                payload=TrackingRequest(
                    dict(tracking_numbers=[instance.tracking_number])
                ).data,
                carrier=carrier,
            )
            # update values only if changed; This is important for webhooks notification
            changes = []
            events = (
                DP.to_dict(response.tracking.events)
                if any(response.tracking.events)
                else instance.events
            )

            if events != instance.events:
                instance.events = events
                changes.append("events")

            if response.messages != instance.messages:
                instance.messages = DP.to_dict(response.messages)
                changes.append("messages")

            if response.tracking.delivered != instance.delivered:
                instance.delivered = response.tracking.delivered
                changes.append("delivered")

            if response.tracking.status != instance.status:
                instance.status = response.tracking.status
                changes.append("status")

            if response.tracking.estimated_delivery != instance.estimated_delivery:
                instance.estimated_delivery = response.tracking.estimated_delivery
                changes.append("estimated_delivery")

            if carrier.id != instance.tracking_carrier.id:
                instance.carrier = carrier
                changes.append("tracking_carrier")

            if any(changes):
                instance.save(update_fields=changes)
                update_shipment_tracker(instance)

        return instance


def update_shipment_tracker(tracker: models.Tracking):
    try:
        if tracker.status == TrackerStatus.delivered.value:
            status = ShipmentStatus.delivered.value
        elif tracker == TrackerStatus.pending.value:
            status = tracker.shipment.status
        else:
            status = ShipmentStatus.in_transit.value

        if tracker.shipment is not None and tracker.shipment.status != status:
            tracker.shipment.status = status
            tracker.shipment.save(update_fields=["status"])
    except Exception as e:
        logger.exception("Failed to update the tracked shipment", e)
