from django.utils import timezone
from rest_framework.serializers import CharField, BooleanField
from purplship.core.utils import DP
from purpleserver.core.gateway import Shipments, Carriers
from purpleserver.core.serializers import TrackingDetails, TrackingRequest

import purpleserver.manager.models as models


class TrackingSerializer(TrackingDetails):
    carrier_id = CharField(required=False)
    carrier_name = CharField(required=False)
    test_mode = BooleanField(required=False)

    def create(self, validated_data: dict) -> models.Tracking:
        created_by = validated_data['created_by']
        carrier_filter = validated_data['carrier_filter']
        tracking_number = validated_data['tracking_number']
        carrier = next(iter(Carriers.list(**carrier_filter)), None)

        response = Shipments.track(
            TrackingRequest(dict(tracking_numbers=[tracking_number])).data,
            carrier_filter=carrier_filter
        )

        return models.Tracking.objects.create(
            created_by=created_by,
            tracking_number=tracking_number,
            events=DP.to_dict(response.tracking.events),
            test_mode=response.tracking.test_mode,
            delivered=response.tracking.delivered,
            tracking_carrier=carrier,
        )

    def update(self, instance: models.Tracking, validated_data) -> models.Tracking:
        last_fetch = (timezone.now() - instance.updated_at).seconds / 60  # minutes since last fetch

        if last_fetch >= 30 and instance.delivered is not True:
            carrier_filter = validated_data['carrier_filter']
            carrier = next(iter(Carriers.list(**carrier_filter)), instance.carrier)
            response = Shipments.track(
                carrier=carrier,
                payload=TrackingRequest(dict(tracking_numbers=[instance.tracking_number])).data
            )
            # update values only if changed; This is important for webhooks notification
            changes = []
            events = DP.to_dict(response.tracking.events)

            if events != instance.events:
                instance.events = events
                changes.append('events')

            if response.tracking.delivered != instance.delivered:
                instance.delivered = response.tracking.delivered
                changes.append('events')

            if carrier.id != instance.tracking_carrier.id:
                instance.carrier = carrier
                changes.append('events')

            if any(changes):
                instance.save(update_fields=changes)

        return instance
