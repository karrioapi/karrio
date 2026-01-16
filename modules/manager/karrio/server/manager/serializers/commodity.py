from rest_framework import status

from karrio.server.core.exceptions import APIException
from karrio.server.core.serializers import CommodityData, ShipmentStatus
from karrio.server.serializers import (
    owned_model_serializer,
    process_dictionaries_mutations,
)
import karrio.server.manager.models as models


@owned_model_serializer
class CommoditySerializer(CommodityData):
    object_type = None

    def create(self, validated_data: dict, **kwargs) -> models.Commodity:
        return models.Commodity.objects.create(**validated_data)

    def update(
        self, instance: models.Commodity, validated_data: dict, **kwargs
    ) -> models.Commodity:
        # Handle dictionary mutations for metadata and meta fields
        data = process_dictionaries_mutations(
            ["metadata", "meta"], validated_data, instance
        )
        changes = []

        for key, val in data.items():
            if getattr(instance, key) != val:
                changes.append(key)
                setattr(instance, key, val)

        instance.save(update_fields=changes)
        return instance


def can_mutate_commodity(
    commodity: models.Commodity, update: bool = False, delete: bool = False, **kwargs
):
    shipment = commodity.shipment
    order = commodity.order

    if shipment is None and order is None:
        return

    if update and shipment and shipment.status != ShipmentStatus.draft.value:
        raise APIException(
            f"Operation not permitted. The related shipment is '{shipment.status}'.",
            status_code=status.HTTP_409_CONFLICT,
            code="state_error",
        )

    if delete and order and len(order.line_items or []) == 1:
        raise APIException(
            f"Operation not permitted. The related order needs at least one line_item.",
            status_code=status.HTTP_409_CONFLICT,
            code="state_error",
        )
