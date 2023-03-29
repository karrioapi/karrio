from django.db import transaction
from rest_framework import status

import karrio.server.manager.models as models
import karrio.server.serializers as serializers
import karrio.server.core.exceptions as exceptions
from karrio.server.core.serializers import CustomsData, ShipmentStatus
from karrio.server.manager.serializers.address import AddressSerializer
from karrio.server.manager.serializers.commodity import CommoditySerializer


@serializers.owned_model_serializer
class CustomsSerializer(CustomsData):
    def __init__(self, instance: models.Customs = None, **kwargs):
        data = kwargs.get("data") or {}

        if ("commodities" in data) and (instance is not None):
            context = getattr(self, "__context", None) or kwargs.get("context")
            serializers.save_many_to_many_data(
                "commodities",
                CommoditySerializer,
                instance,
                payload=data,
                context=context,
                partial=True,
            )

        super().__init__(instance, **kwargs)

    @transaction.atomic
    def create(self, validated_data: dict, context: dict, **kwargs) -> models.Customs:
        instance = models.Customs.objects.create(
            **{
                **{
                    key: value
                    for key, value in validated_data.items()
                    if key in models.Customs.DIRECT_PROPS
                },
                "duty_billing_address": serializers.save_one_to_one_data(
                    "duty_billing_address",
                    AddressSerializer,
                    payload=validated_data,
                    context=context,
                ),
            }
        )

        serializers.save_many_to_many_data(
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
        data = serializers.process_dictionaries_mutations(
            ["options"], validated_data, instance
        )
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
        raise exceptions.APIException(
            f"Operation not permitted. The related shipment is '{shipment.status}'.",
            status_code=status.HTTP_409_CONFLICT,
            code="state_error",
        )
