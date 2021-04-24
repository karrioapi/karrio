from django.db import transaction

from purpleserver.core.utils import SerializerDecorator
from purpleserver.core.serializers import PaymentData

from purpleserver.manager.serializers.address import AddressSerializer
import purpleserver.manager.models as models


class PaymentSerializer(PaymentData):

    def __init__(self, *args, **kwargs):
        if kwargs.get('data') is not None:
            if isinstance(kwargs['data'], str):
                payload = PaymentData(models.Payment.objects.get(pk=kwargs['data'])).data

            else:
                payload = kwargs['data'].copy()
                if payload.get('contact') is not None:
                    payload.update(
                        payment=SerializerDecorator[AddressSerializer](data=payload['contact']).data
                    )

            kwargs.update(data=payload)

        super().__init__(*args, **kwargs)

    @transaction.atomic
    def create(self, validated_data: dict) -> models.Payment:
        created_by = validated_data['created_by']
        data = {
            key: value for key, value in validated_data.items() if key in models.Payment.DIRECT_PROPS
        }

        related_data = dict(
            contact=SerializerDecorator[AddressSerializer](
                data=validated_data.get('contact')).save(created_by=created_by).instance,
        )

        payment = models.Payment.objects.create(**{
            **data,
            **related_data,
            'created_by': created_by
        })
        return payment

    @transaction.atomic
    def update(self, instance: models.Payment, validated_data: dict) -> models.Payment:
        created_by = validated_data.get('created_by', instance.created_by)
        for key, val in validated_data.items():
            if key in models.Payment.DIRECT_PROPS:
                setattr(instance, key, val)

        if validated_data.get('contact') is not None:
            data = validated_data.get('contact')
            if instance.contact is not None and data is None:
                instance.contact.delete()
                instance.contact = None
            else:
                instance.contact = SerializerDecorator[AddressSerializer](
                    instance.contact, data=data).save(created_by=created_by).instance

        instance.save()
        return instance
