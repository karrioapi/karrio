from django.db import transaction
from rest_framework.reverse import reverse
from rest_framework.serializers import Serializer, CharField, ChoiceField, BooleanField

from purplship.core.utils import to_dict
from purpleserver.core.gateway import Shipments
from purpleserver.core.utils import SerializerDecorator
from purpleserver.core.datatypes import RateResponse, ShipmentResponse, Confirmation, ConfirmationResponse
from purpleserver.providers.models import Carrier
from purpleserver.core.serializers import (
    SHIPMENT_STATUS,
    ShipmentStatus,
    ShipmentData,
    Shipment,
    Payment,
    Rate,
    ShippingRequest,
    ShipmentCancelRequest,
)
from purpleserver.manager.serializers.address import AddressSerializer
from purpleserver.manager.serializers.payment import PaymentSerializer
from purpleserver.manager.serializers.customs import CustomsSerializer
from purpleserver.manager.serializers.parcel import ParcelSerializer
from purpleserver.manager.serializers.rate import RateSerializer
import purpleserver.manager.models as models


class ShipmentSerializer(ShipmentData):
    status = ChoiceField(required=False, choices=SHIPMENT_STATUS)
    selected_rate_id = CharField(required=False)
    rates = Rate(many=True, required=False)
    label = CharField(required=False, allow_blank=True, allow_null=True)
    tracking_number = CharField(required=False, allow_blank=True, allow_null=True)
    shipment_identifier = CharField(required=False, allow_blank=True, allow_null=True)
    selected_rate = Rate(required=False, allow_null=True)
    tracking_url = CharField(required=False, allow_blank=True, allow_null=True)
    test_mode = BooleanField(required=False)

    def __init__(self, instance: models.Shipment = None, **kwargs):
        if kwargs.get('data') is not None:
            if isinstance(kwargs['data'], str):
                payload = ShipmentData(models.Shipment.objects.get(pk=kwargs['data'])).data

            else:
                payload = kwargs['data'].copy()
                if payload.get('shipper') is not None:
                    payload.update(
                        shipper=SerializerDecorator[AddressSerializer](
                            (instance.shipper if instance is not None else None),
                            data=payload['shipper']
                        ).data
                    )

                if payload.get('recipient') is not None:
                    payload.update(
                        recipient=SerializerDecorator[AddressSerializer](
                            (instance.recipient if instance is not None else None),
                            data=payload['recipient']
                        ).data
                    )

                if payload.get('parcels') is not None:
                    payload.update(
                        parcels=[
                            SerializerDecorator[ParcelSerializer](data=parcel).data
                            for parcel in payload.get('parcels', [])
                        ]
                    )

                if payload.get('customs') is not None:
                    payload.update(
                        customs=SerializerDecorator[CustomsSerializer](
                            (instance.customs if instance is not None else None),
                            data=payload['customs']
                        ).data
                    )

                if payload.get('payment') is not None:
                    payload.update(
                        payment=SerializerDecorator[PaymentSerializer](
                            (instance.payment if instance is not None else None),
                            data=payload['payment']
                        ).data
                    )

            kwargs.update(data=payload)

        super().__init__(instance, **kwargs)

    @transaction.atomic
    def create(self, validated_data: dict) -> models.Shipment:
        carriers = Carrier.objects.filter(carrier_id__in=validated_data.get('carrier_ids', []))
        rate_response: RateResponse = SerializerDecorator[RateSerializer](data=validated_data).save().instance
        test_mode = all([r.test_mode for r in rate_response.rates])
        user = validated_data['user']

        shipment_data = {
            key: value for key, value in validated_data.items()
            if key in models.Shipment.DIRECT_PROPS and value is not None
        }

        related_data = dict(
            shipper=SerializerDecorator[AddressSerializer](
                data=validated_data.get('shipper')).save(user=user).instance,

            recipient=SerializerDecorator[AddressSerializer](
                data=validated_data.get('recipient')).save(user=user).instance,

            customs=SerializerDecorator[CustomsSerializer](
                data=validated_data.get('customs')).save(user=user).instance,

            payment=SerializerDecorator[PaymentSerializer](
                data=validated_data.get('payment')).save(user=user).instance,
        )

        shipment = models.Shipment.objects.create(**{
            **shipment_data,
            **{k: v for k, v in related_data.items() if v is not None},
            'user': user,
            'test_mode': test_mode,
            'shipment_rates': to_dict(rate_response.rates),
        })
        shipment.carriers.set(carriers)

        if validated_data.get('parcels') is not None:
            shipment_parcels = [
                SerializerDecorator[ParcelSerializer](data=data).save(user=validated_data['user']).instance
                for data in validated_data.get('parcels', [])
            ]
            shipment.shipment_parcels.set(shipment_parcels)

        return shipment

    @transaction.atomic
    def update(self, instance: models.Shipment, validated_data: dict) -> models.Shipment:
        data = validated_data.copy()
        carrier_ids = validated_data.get('carrier_ids', [])

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

        if validated_data.get('payment') is not None:
            instance.payment = SerializerDecorator[PaymentSerializer](
                instance.payment, data=validated_data['payment']).save(user=instance.user).instance

        if validated_data.get('customs') is not None:
            instance.customs = SerializerDecorator[CustomsSerializer](
                data=validated_data.get('customs')).save(user=instance.user).instance

        if validated_data.get('rates') is not None:
            instance.shipment_rates = to_dict(validated_data.get('rates', []))

        if validated_data.get('selected_rate') is not None:
            selected_rate = validated_data.get('selected_rate')
            carrier = Carrier.objects.get(carrier_id=selected_rate['carrier_id'])

            instance.selected_rate = {**selected_rate, 'carrier_ref': carrier.id}
            instance.selected_rate_carrier = carrier

        instance.save()
        instance.carriers.set(Carrier.objects.filter(carrier_id__in=carrier_ids))
        return instance


class ShipmentPurchaseData(Serializer):
    selected_rate_id = CharField(required=True, help_text="The shipment selected rate.")
    payment = Payment(required=False, help_text="The payment details")


class ShipmentValidationData(Shipment):
    rates = Rate(many=True, required=True)
    payment = Payment(required=True)

    def create(self, validated_data: dict) -> ShipmentResponse:
        return Shipments.create(
            ShippingRequest(validated_data).data,
            resolve_tracking_url=(
                lambda shipment: reverse(
                    "purpleserver.manager:shipment-tracking",
                    kwargs=dict(tracking_number=shipment.tracking_number, carrier_name=shipment.carrier_name)
                )
            )
        )


class ShipmentCancelSerializer(Shipment):

    def update(self, instance: models.Shipment, validated_data: dict) -> ConfirmationResponse:
        if instance.status == ShipmentStatus.purchased.value:
            response = Shipments.cancel(
                payload=ShipmentCancelRequest(instance).data,
                carrier=instance.selected_rate_carrier
            )
        else:
            response = ConfirmationResponse(
                messages=[],
                confirmation=Confirmation(
                    carrier_name="None Selected",
                    carrier_id="None Selected",
                    success=True,
                    operation="Cancel Shipment",
                )
            )

        instance.delete()
        return response
