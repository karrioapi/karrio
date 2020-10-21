from rest_framework import serializers

from purpleserver.core.utils import SerializerDecorator
from purpleserver.core.gateway import Pickups, Carriers
from purpleserver.core.datatypes import Confirmation
from purpleserver.core.serializers import (
    AddressData,
    PickupRequest,
    PickupUpdateRequest,
    PickupCancelRequest,
    StringListField,
)
from purpleserver.manager.serializers import AddressSerializer
import purpleserver.manager.models as models


def shipment_exists(value):
    validation = {
        key: models.Shipment.objects.filter(tracking_number=key).exists() for key in value
    }
    if not all(validation.values()):
        invalids = [key for key, val in validation.items() if val is False]
        raise serializers.ValidationError(f"Shipment with the tracking numbers: {invalids} not found", code="invalid")


def address_exists(value):
    if value is str and not models.Address.objects.filter(pk=value).exists():
        raise serializers.ValidationError(f"Address with id {value} not found: {value}", code="invalid")


class PickupSerializer(PickupRequest):
    parcels = None
    address = AddressData(
        required=False,
        validators=[address_exists],
        help_text="The pickup address")
    tracking_numbers = StringListField(
        required=True,
        validators=[shipment_exists],
        help_text="The list of shipments to be picked up")

    def __init__(self, instance: models.Pickup = None, **kwargs):
        if 'data' in kwargs:
            data = kwargs.get('data').copy()

            self._shipments = models.Shipment.objects.filter(tracking_number__in=data.get('tracking_numbers', []))

            if data.get('address') is None and instance is None:
                address = next((AddressData(s.shipper).data for s in self._shipments), None)
            elif data.get('address') is None and instance is not None:
                address = AddressData(instance.address).data
            elif data.get('address') is str:
                address = models.Shipment.objects.get(pk=data.get('address'))
            else:
                address = data.get('address')

            if address is not None:
                self._address = SerializerDecorator[AddressSerializer](
                    (None if instance is None else instance.address), data=address)
                data.update(address=self._address.data)

            kwargs.update(data=data)

        super().__init__(instance, **kwargs)

    def validate(self, data):
        validated_data = super(PickupSerializer, self).validate(data)

        if len(validated_data.get('tracking_numbers', [])) > 1 and validated_data.get('address') is None:
            raise serializers.ValidationError("address must be specified for multi-shipments pickup", code="required")

        return validated_data

    def create(self, validated_data: dict) -> models.Pickup:
        user = validated_data["user"]
        carrier_filter = validated_data["carrier_filter"]
        carrier = next(iter(Carriers.list(**carrier_filter)), None)
        request_data = PickupRequest({
            **validated_data,
            "address": self._address.data,
            "parcels": sum([list(s.parcels) for s in self._shipments], [])
        }).data

        response = Pickups.schedule(payload=request_data, carrier=carrier)
        payload = {
            key: value for key, value in validated_data.items()
            if key in models.Pickup.DIRECT_PROPS
        }
        address = self._address.save(user=validated_data["user"]).instance

        pickup = models.Pickup.objects.create(**{
            **payload,
            "user": user,
            "address": address,
            "pickup_carrier": carrier,
            "test_mode": response.pickup.test_mode,
            "confirmation_number": response.pickup.confirmation_number,
        })
        pickup.shipments.set(self._shipments)

        return pickup

    def update(self, instance: models.Pickup, validated_data) -> models.Tracking:
        request_data = SerializerDecorator[PickupUpdateRequest](data={
            **PickupUpdateRequest(instance).data,
            **validated_data,
            "address": AddressData({
                **AddressData(instance.address).data,
                **validated_data['address']
            }).data
        })

        Pickups.update(payload=request_data.data, carrier=instance.pickup_carrier)

        data = validated_data.copy()
        for key, val in data.items():
            if key in models.Pickup.DIRECT_PROPS:
                setattr(instance, key, val)
                validated_data.pop(key)

        self._address.save()
        instance.save()
        return instance


class PickupData(PickupSerializer):
    pass


class PickupUpdateData(PickupData):
    confirmation_number = serializers.CharField(required=True, help_text="pickup identification number")
    pickup_date = serializers.CharField(required=False, help_text="""
    The expected pickup date
    
    Date Format: YYYY-MM-DD
    """)
    ready_time = serializers.CharField(required=False, allow_blank=True, allow_null=True, help_text="The ready time for pickup.")
    closing_time = serializers.CharField(required=False, allow_blank=True, allow_null=True, help_text="The closing or late time of the pickup")
    instruction = serializers.CharField(required=False, allow_blank=True, allow_null=True, help_text="""
    The pickup instruction.
    
    eg: Handle with care.
    """)
    package_location = serializers.CharField(required=False, allow_blank=True, allow_null=True, help_text="""
    The package(s) location.
    
    eg: Behind the entrance door.
    """)
    tracking_numbers = StringListField(
        required=False,
        validators=[shipment_exists],
        help_text="The list of shipments to be picked up")


class PickupCancelData(serializers.Serializer):
    reason = serializers.CharField(required=False, help_text="The reason of the pickup cancellation")

    def update(self, instance: models.Pickup, validated_data) -> Confirmation:
        request = PickupCancelRequest({
            **PickupCancelRequest(instance).data,
            **validated_data
        })
        response = Pickups.cancel(payload=request.data, carrier=instance.pickup_carrier)
        instance.delete()

        return response.confirmation
