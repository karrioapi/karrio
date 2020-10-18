from django.utils import timezone
from rest_framework.serializers import CharField, BooleanField
from purplship.core.utils import to_dict
from purpleserver.core.gateway import Shipments
from purpleserver.core.serializers import TrackingDetails, TrackingRequest

import purpleserver.manager.models as models


class TrackingSerializer(TrackingDetails):
    carrier_name = CharField(required=False)
    test_mode = BooleanField(required=False)

    def create(self, validated_data: dict) -> models.Tracking:
        user = validated_data['user']
        carrier_id = validated_data['carrier_id']
        shipment_id = validated_data.get('shipment_id')
        tracking_number = validated_data['tracking_number']

        response = Shipments.track(
            carrier_filter=dict(carrier_id=carrier_id),
            payload=TrackingRequest(dict(tracking_numbers=[tracking_number])).data
        )

        return models.Tracking.objects.create(
            user=user,
            tracking_number=tracking_number,
            events=to_dict(response.tracking.events),
            test_mode=response.tracking.test_mode,
            tracking_carrier=models.Carrier.objects.get(carrier_id=carrier_id),
            tracking_shipment=models.Shipment.objects.filter(id=shipment_id).first(),
        )

    def update(self, instance: models.Tracking, validated_data) -> models.Tracking:
        last_fetch = (timezone.now() - instance.updated_at).seconds / 60  # minutes since last fetch

        if last_fetch >= 30:
            response = Shipments.track(
                carrier_filter=dict(carrier_id=instance.carrier_id),
                payload=TrackingRequest(dict(tracking_numbers=[instance.tracking_number])).data
            )
            instance.events = to_dict(response.tracking.events)
            instance.save()

        return instance
