from rest_framework import status

from karrio.server.core.exceptions import APIException
from karrio.server.core.serializers import ParcelData, ShipmentStatus
from karrio.server.serializers import (
    owned_model_serializer,
    save_many_to_many_data,
    process_dictionaries_mutations,
)

from karrio.server.manager.serializers.commodity import CommoditySerializer
import karrio.server.manager.models as models


@owned_model_serializer
class ParcelSerializer(ParcelData):
    object_type = None

    def __init__(self, instance: models.Address = None, **kwargs):
        data = kwargs.get("data") or {}

        if ("items" in data) and (instance is not None):
            context = getattr(self, "__context", None) or kwargs.get("context")
            save_many_to_many_data(
                "items",
                CommoditySerializer,
                instance,
                payload=data,
                context=context,
            )

        super().__init__(instance, **kwargs)

    def create(self, validated_data: dict, context: dict, **kwargs) -> models.Parcel:
        instance = models.Parcel.objects.create(
            **{key: value for key, value in validated_data.items() if key != "items"}
        )

        save_many_to_many_data(
            "items",
            CommoditySerializer,
            instance,
            payload=validated_data,
            context=context,
        )

        return instance

    def update(
        self, instance: models.Parcel, validated_data: dict, **kwargs
    ) -> models.Parcel:
        data = process_dictionaries_mutations(["options"], validated_data, instance)
        changes = []

        for key, val in data.items():
            if getattr(instance, key) != val and key != "items":
                changes.append(key)
                setattr(instance, key, val)

        instance.save(update_fields=changes)
        return instance


def can_mutate_parcel(
    parcel: models.Parcel, update: bool = False, delete: bool = False, **kwargs
):
    shipment = parcel.shipment

    if shipment is None:
        return

    if update and shipment.status != ShipmentStatus.draft.value:
        raise APIException(
            f"Operation not permitted. The related shipment is '{shipment.status}'.",
            status_code=status.HTTP_409_CONFLICT,
            code="state_error",
        )

    if delete and len(shipment.parcels.all()) == 1:
        raise APIException(
            f"Operation not permitted. The related shipment needs at least one parcel.",
            status_code=status.HTTP_409_CONFLICT,
            code="state_error",
        )
