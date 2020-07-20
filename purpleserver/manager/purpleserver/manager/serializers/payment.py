from django.db import transaction

from purpleserver.core.utils import validate_and_save
from purpleserver.core.serializers import PaymentData, AddressData

from purpleserver.manager.serializers.address import AddressSerializer
import purpleserver.manager.models as models


class PaymentSerializer(PaymentData):

    def __init__(self, *args, **kwargs):
        if 'data' in kwargs:
            payload = kwargs['data'].copy()

            if 'contact' in payload:
                payload.update(
                    shipper=(
                        AddressData(models.Address.objects.get(pk=payload.get('contact'))).data
                        if isinstance(payload.get('contact'), str) else
                        payload.get('contact')
                    )
                )

            kwargs.update(data=payload)

        super().__init__(*args, **kwargs)

    @transaction.atomic
    def create(self, validated_data: dict) -> models.Payment:
        data = {
            key: value for key, value in validated_data.items() if key in models.Payment.DIRECT_PROPS
        }

        related_data = dict(
            contact=validate_and_save(
                AddressSerializer, validated_data.get('contact'), user=validated_data['user']
            ),
        )

        payment = models.Payment.objects.create(**{
            **data,
            **related_data,
            'user': validated_data['user']
        })
        return payment

    @transaction.atomic
    def update(self, instance: models.Payment, validated_data: dict) -> models.Payment:
        for key, val in validated_data.items():
            if key in models.Payment.DIRECT_PROPS:
                setattr(instance, key, val)

        if 'contact' in validated_data:
            data = validated_data.get('contact')
            if instance.contact is not None and data is None:
                instance.contact.delete()
                instance.contact = None
            else:
                instance.contact = validate_and_save(
                    AddressSerializer, data, instance=instance.contact, user=validated_data['user'])

        instance.save()
        return instance
