from typing import List
from django.db import transaction
from rest_framework.reverse import reverse
from rest_framework.serializers import Serializer, CharField

from purplship.core.utils import to_dict
from purpleserver.core.gateway import Shipments
from purpleserver.core.utils import validate_and_save
from purpleserver.carriers.models import Carrier
from purpleserver.core.serializers import (
    ShipmentData,
    ShipmentResponse,
    Shipment,
    Payment,
    ListField,
    URLField,
    Rate,
    AddressData,
    ParcelData,
    PaymentData,
    CustomsData,
    ShippingRequest
)
from purpleserver.manager.serializers.address import AddressSerializer
from purpleserver.manager.serializers.payment import PaymentSerializer
from purpleserver.manager.serializers.customs import CustomsSerializer
from purpleserver.manager.serializers.parcel import ParcelSerializer
import purpleserver.manager.models as models


class ShipmentSerializer(ShipmentData):
    selected_rate_id = CharField(required=False)
    rates = ListField(child=Rate(), required=False)
    label = CharField(required=False, allow_blank=True, allow_null=True)
    tracking_number = CharField(required=False, allow_blank=True, allow_null=True)
    selected_rate = Rate(required=False, allow_null=True)
    tracking_url = URLField(required=False, allow_blank=True, allow_null=True)

    def __init__(self, *args, **kwargs):
        if 'data' in kwargs:
            payload = kwargs['data'].copy()
            if 'shipper' in payload:
                payload.update(
                    shipper=(
                        AddressData(models.Address.objects.get(pk=payload.get('shipper'))).data
                        if isinstance(payload.get('shipper'), str) else
                        payload.get('shipper')
                    )
                )

            if 'recipient' in payload:
                payload.update(
                    recipient=(
                        AddressData(models.Address.objects.get(pk=payload.get('recipient'))).data
                        if isinstance(payload.get('recipient'), str) else
                        payload.get('recipient')
                    )
                )

            if 'parcel' in payload:
                payload.update(
                    parcel=(
                        ParcelData(models.Parcel.objects.get(pk=payload.get('parcel'))).data
                        if isinstance(payload.get('parcel'), str) else
                        payload.get('parcel')
                    )
                )

            if 'customs' in payload:
                payload.update(
                    customs=(
                        CustomsData(models.Customs.objects.get(pk=payload.get('customs'))).data
                        if isinstance(payload.get('customs'), str) else
                        payload.get('customs')
                    )
                )

            if 'payment' in payload:
                payload.update(
                    payment=(
                        PaymentData(models.Payment.objects.get(pk=payload.get('payment'))).data
                        if isinstance(payload.get('payment'), str) else
                        payload.get('payment')
                    )
                )

            kwargs.update(data=payload)

        super().__init__(*args, **kwargs)

    @transaction.atomic
    def create(self, validated_data: dict) -> models.Shipment:
        carriers = Carrier.objects.filter(carrier_id__in=validated_data.get('carrier_ids', []))

        shipment_data = {
            key: value for key, value in validated_data.items()
            if key in models.Shipment.DIRECT_PROPS and value is not None
        }

        related_data = dict(
            shipper=validate_and_save(
                AddressSerializer, validated_data.get('shipper'), user=validated_data['user']
            ),
            recipient=validate_and_save(
                AddressSerializer, validated_data.get('recipient'), user=validated_data['user']
            ),
            parcel=validate_and_save(
                ParcelSerializer, validated_data.get('parcel'), user=validated_data['user']
            ),
            customs=validate_and_save(
                CustomsSerializer, validated_data.get('customs'), user=validated_data['user']
            ),
            payment=validate_and_save(
                PaymentSerializer, validated_data.get('payment'), user=validated_data['user']
            ),
        )

        shipment = models.Shipment.objects.create(**{
            **shipment_data,
            **{k: v for k, v in related_data.items() if v is not None},
            'user': validated_data['user']
        })
        shipment.carriers.set(carriers)
        return shipment

    @transaction.atomic
    def update(self, instance: models.Shipment, validated_data: dict) -> models.Shipment:
        data = validated_data.copy()
        carrier_ids = validated_data.get('carrier_ids', [])
        carriers: List[Carrier] = Carrier.objects.filter(carrier_id__in=carrier_ids)

        for key, val in data.items():
            if key in models.Shipment.DIRECT_PROPS:
                setattr(instance, key, val)
                validated_data.pop(key)

            if key in models.Shipment.RELATIONAL_PROPS and val is None:
                prop = getattr(instance, key)
                # Delete related data from database if payload set to null
                if hasattr(prop, 'delete'):
                    prop.delete()
                    setattr(instance, key, None)
                    validated_data.pop(key)

        if 'shipper' in validated_data:
            validate_and_save(AddressSerializer, validated_data.get('shipper', {}), instance=instance.shipper)

        if 'recipient' in validated_data:
            validate_and_save(AddressSerializer, validated_data.get('recipient', {}), instance=instance.recipient)

        if 'parcel' in validated_data:
            validate_and_save(ParcelSerializer, validated_data.get('parcel', {}), instance=instance.parcel)

        if 'customs' in validated_data:
            instance.customs = validate_and_save(
                CustomsSerializer, validated_data.get('customs', {}), instance=instance.customs, user=instance.user
            )

        if 'payment' in validated_data:
            instance.payment = validate_and_save(
                PaymentSerializer, validated_data.get('payment', {}), instance=instance.payment, user=instance.user
            )

        if 'rates' in validated_data:
            instance.shipment_rates = to_dict(validated_data.get('rates', []))

        if 'selected_rate' in validated_data:
            selected_rate = validated_data.get('selected_rate')
            carrier = Carrier.objects.get(carrier_id=selected_rate['carrier_id'])

            setattr(instance, 'selected_rate_carrier', carrier)
            setattr(instance, 'selected_rate', {**selected_rate, 'carrier_ref': carrier.id})

        instance.save()
        instance.carriers.set(carriers)
        return instance


class ShipmentPurchaseData(Serializer):
    selected_rate_id = CharField(required=True, help_text="The shipment selected rate.")
    payment = Payment(required=False, help_text="The payment details")


class ShipmentValidationData(Shipment):
    rates = ListField(required=True, child=Rate())
    payment = Payment(required=True)

    def create(self, validated_data: dict) -> ShipmentResponse:
        return Shipments.create(
            ShippingRequest(validated_data).data,
            resolve_tracking_url=(
                lambda trackin_url, shipping: reverse(
                    "purpleserver.proxy:TrackShipment",
                    request=validated_data.get('request'),
                    kwargs=dict(tracking_number=shipping.tracking_number, carrier_name=shipping.carrier_name)
                )
            )
        )
