from django.db import transaction
from rest_framework import status

from karrio.server.core.exceptions import APIException
from karrio.server.serializers import (
    save_many_to_many_data,
    owned_model_serializer,
    process_dictionaries_mutations,
)
from karrio.server.core.serializers import CustomsData, ShipmentStatus

from karrio.server.manager.serializers.commodity import CommoditySerializer
import karrio.server.manager.models as models


@owned_model_serializer
class CustomsSerializer(CustomsData):
    def __init__(self, instance: models.Customs = None, **kwargs):
        data = kwargs.get("data") or {}

        if ("commodities" in data) and (instance is not None):
            context = getattr(self, "__context", None) or kwargs.get("context")
            save_many_to_many_data(
                "commodities",
                CommoditySerializer,
                instance,
                payload=data,
                context=context,
            )

        super().__init__(instance, **kwargs)

    @transaction.atomic
    def create(self, validated_data: dict, context: dict, **kwargs) -> models.Customs:
        instance = models.Customs.objects.create(
            **{
                key: value
                for key, value in validated_data.items()
                if key in models.Customs.DIRECT_PROPS
            }
        )

        save_many_to_many_data(
            "commodities",
            CommoditySerializer,
            instance,
            payload=validated_data,
            context=context,
        )

        return instance

    @transaction.atomic
    def update(
        self, instance: models.Customs, validated_data: dict, **kwargs
    ) -> models.Customs:
        data = process_dictionaries_mutations(["options"], validated_data, instance)
        changes = []

        for key, val in data.items():
            if key in models.Customs.DIRECT_PROPS and getattr(instance, key) != val:
                changes.append(key)
                setattr(instance, key, val)

        instance.save(update_fields=changes)
        return instance


def can_mutate_customs(customs: models.Customs, **kwargs):
    shipment = customs.shipment

    if shipment is not None and shipment.status != ShipmentStatus.create.value:
        raise APIException(
            f"Operation not permitted. The related shipment is '{shipment.status}'.",
            status_code=status.HTTP_409_CONFLICT,
            code="state_error",
        )
