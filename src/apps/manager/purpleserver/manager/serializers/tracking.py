from django.utils import timezone
from rest_framework.serializers import CharField, BooleanField
from purplship.core.utils import to_dict
from purpleserver.core.gateway import Shipments, Carriers
from purpleserver.core.serializers import TrackingDetails, TrackingRequest

import purpleserver.manager.models as models


class TrackingSerializer(TrackingDetails):
    carrier_id = CharField(required=False)
    carrier_name = CharField(required=False)
    test_mode = BooleanField(required=False)

    def create(self, validated_data: dict) -> models.Tracking:
        user = validated_data['user']
        carrier_filter = validated_data['carrier_filter']
        tracking_number = validated_data['tracking_number']
        carrier = next(iter(Carriers.list(**carrier_filter)), None)

        response = Shipments.track(
            carrier=carrier,
            payload=TrackingRequest(dict(tracking_numbers=[tracking_number])).data
        )

        return models.Tracking.objects.create(
            user=user,
            tracking_number=tracking_number,
            events=to_dict(response.tracking.events),
            test_mode=response.tracking.test_mode,
            tracking_carrier=carrier,
        )

    def update(self, instance: models.Tracking, validated_data) -> models.Tracking:
        last_fetch = (timezone.now() - instance.updated_at).seconds / 60  # minutes since last fetch

        if last_fetch >= 30:
            carrier = next(iter(Carriers.list(**validated_data['carrier_filter'])), None)
            response = Shipments.track(
                carrier=carrier,
                payload=TrackingRequest(dict(tracking_numbers=[instance.tracking_number])).data
            )
            instance.events = to_dict(response.tracking.events)
            instance.carrier = carrier
            instance.save()

        return instance
