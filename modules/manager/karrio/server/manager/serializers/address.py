from rest_framework import status

from karrio.server.core.exceptions import APIException
from karrio.server.serializers import owned_model_serializer
from karrio.core import utils
from karrio.server.core import gateway
from karrio.server.core.serializers import AddressData, ShipmentStatus
from karrio.server.manager import models


@owned_model_serializer
class AddressSerializer(AddressData):
    def validate(self, data):
        validated_data = super().validate(data)
        should_validate = validated_data.get("validate_location") is True or (
            self.instance is not None and self.instance.validate_location
        )

        if should_validate:
            address = {
                **(
                    AddressData(self.instance).data if self.instance is not None else {}
                ),
                **validated_data,
            }
            validation = gateway.Address.validate(address)
            validated_data.update(dict(validation=utils.DP.to_dict(validation)))

        return validated_data

    def create(self, validated_data: dict, **kwargs) -> models.Address:
        return models.Address.objects.create(**validated_data)

    def update(
        self, instance: models.Address, validated_data: dict, **kwargs
    ) -> models.Address:
        changes = []
        for key, val in validated_data.items():
            if getattr(instance, key) != val:
                changes.append(key)
                setattr(instance, key, val)

        instance.save(update_fields=changes)
        return instance


def can_mutate_address(
    address: models.Address, update: bool = False, delete: bool = False
):
    shipment = address.shipment
    order = address.order

    if shipment is None and order is None:
        return

    if update and shipment and shipment.status != ShipmentStatus.draft.value:
        raise APIException(
            f"Operation not permitted. The related shipment is '{shipment.status}'.",
            status_code=status.HTTP_409_CONFLICT,
            code="state_error",
        )

    if delete and shipment is not None:
        raise APIException(
            "This address is linked to a shipment and cannot be removed",
            status_code=status.HTTP_409_CONFLICT,
            code="state_error",
        )

    if update and order and order.status != "unfulfilled":
        raise APIException(
            f"Operation not permitted. The related order is '{order.status}'.",
            status_code=status.HTTP_409_CONFLICT,
            code="state_error",
        )

    if delete and order is not None:
        raise APIException(
            "This address is linked to an order and cannot be removed",
            status_code=status.HTTP_409_CONFLICT,
            code="state_error",
        )
