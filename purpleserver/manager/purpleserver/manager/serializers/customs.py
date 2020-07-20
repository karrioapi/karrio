from django.db import transaction

from purpleserver.core.utils import validate_and_save
from purpleserver.core.serializers import CustomsData, PaymentData, CommodityData

from purpleserver.manager.serializers.payment import PaymentSerializer
from purpleserver.manager.serializers.commodity import CommoditySerializer
import purpleserver.manager.models as models


class CustomsSerializer(CustomsData):

    def __init__(self, *args, **kwargs):
        if 'data' in kwargs:
            payload = kwargs['data'].copy()

            if 'duty' in payload:
                payload.update(
                    payment=(
                        PaymentData(models.Payment.objects.get(pk=payload.get('duty'))).data
                        if isinstance(payload.get('duty'), str) else
                        payload.get('duty')
                    )
                )

            if 'commodities' in payload:
                payload.update(
                    commodities=[
                        (
                            CommodityData(models.Commodity.objects.get(pk=commodity)).data
                            if isinstance(commodity, str) else commodity
                        )
                        for commodity in payload.get('commodities', [])
                    ]
                )

            kwargs.update(data=payload)

        super().__init__(*args, **kwargs)

    @transaction.atomic
    def create(self, validated_data: dict) -> models.Customs:
        related_data = {}
        data = {
            key: value for key, value in validated_data.items() if key in models.Customs.DIRECT_PROPS
        }

        if 'duty' in validated_data:
            related_data = dict(
                duty=validate_and_save(
                    PaymentSerializer, validated_data.get('duty'), user=validated_data['user']
                ),
            )

        customs = models.Customs.objects.create(**{
            **data,
            **related_data,
            'user': validated_data['user']
        })

        if 'commodities' in validated_data:
            shipment_commodities = [
                validate_and_save(CommoditySerializer, data, user=validated_data['user'])
                for data in validated_data.get('commodities', [])
            ]
            customs.shipment_commodities.set(shipment_commodities)

        return customs

    @transaction.atomic
    def update(self, instance: models.Customs, validated_data: dict) -> models.Customs:
        for key, val in validated_data.items():
            if key in models.Customs.DIRECT_PROPS:
                setattr(instance, key, val)

        if 'duty' in validated_data:
            data = validated_data.get('duty')
            if instance.duty is not None and data is None:
                instance.duty.delete()
                instance.duty = None
            else:
                instance.duty = validate_and_save(
                    PaymentSerializer, data, instance=instance.duty, user=validated_data['user'])

        if 'commodities' in validated_data:
            instance.commodities.all().delete()
            instance.commodities.set([
                validate_and_save(CommoditySerializer, data, user=validated_data['user'])
                for data in validated_data.get('commodities', []) or []
            ])

        instance.save()
        return instance
