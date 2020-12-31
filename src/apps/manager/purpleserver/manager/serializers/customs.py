from django.db import transaction

from purpleserver.core.utils import SerializerDecorator
from purpleserver.core.serializers import CustomsData

from purpleserver.manager.serializers.payment import PaymentSerializer
from purpleserver.manager.serializers.commodity import CommoditySerializer
import purpleserver.manager.models as models


class CustomsSerializer(CustomsData):

    def __init__(self, instance: models.Customs = None, **kwargs):
        if kwargs.get('data') is not None:
            if isinstance(kwargs['data'], str):
                payload = CustomsData(models.Customs.objects.get(pk=kwargs['data'])).data

            else:
                payload = kwargs['data'].copy()
                if payload.get('duty') is not None:
                    payload.update(
                        payment=SerializerDecorator[PaymentSerializer](
                            data=payload['duty']
                        ).data
                    )

                if payload.get('commodities') is not None:
                    payload.update(
                        commodities=[
                            SerializerDecorator[CommoditySerializer](data=commodity).data
                            for commodity in payload.get('commodities', [])
                        ]
                    )

            kwargs.update(data=payload)

        super().__init__(instance, **kwargs)

    @transaction.atomic
    def create(self, validated_data: dict) -> models.Customs:
        user = validated_data['user']
        related_data = {}
        data = {
            key: value for key, value in validated_data.items() if key in models.Customs.DIRECT_PROPS
        }

        if validated_data.get('duty') is not None:
            related_data = dict(
                duty=SerializerDecorator[PaymentSerializer](
                    data=validated_data.get('duty')).save(user=user).instance)

        customs = models.Customs.objects.create(**{
            **data,
            **related_data,
            'user': user
        })

        if validated_data.get('commodities') is not None:
            shipment_commodities = [
                SerializerDecorator[CommoditySerializer](data=data).save(user=user).instance
                for data in validated_data.get('commodities', [])
            ]
            customs.shipment_commodities.set(shipment_commodities)

        return customs

    @transaction.atomic
    def update(self, instance: models.Customs, validated_data: dict) -> models.Customs:
        user = validated_data.get('user', instance.user)
        for key, val in validated_data.items():
            if key in models.Customs.DIRECT_PROPS:
                setattr(instance, key, val)

        if 'duty' in validated_data:
            data = validated_data.get('duty')
            if instance.duty is not None and data is None:
                instance.duty.delete()
                instance.duty = None
            else:
                instance.duty = SerializerDecorator[PaymentSerializer](
                    instance.duty, data=data).save(user=user).instance

        instance.save()
        return instance
