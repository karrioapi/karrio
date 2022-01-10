from rest_framework import status
from django.conf import settings
from django.db.models import Q


from purplship.server.core.exceptions import PurplshipAPIException
from purplship.server.core.serializers import Commodity, CommodityData, ShipmentStatus
from purplship.server.serializers import owned_model_serializer
import purplship.server.manager.models as models


@owned_model_serializer
class CommoditySerializer(Commodity):
    def create(self, validated_data: dict, **kwargs) -> Commodity:
        return models.Commodity.objects.create(**validated_data)

    def update(
        self, instance: models.Commodity, validated_data: dict, **kwargs
    ) -> models.Commodity:
        for key, val in validated_data.items():
            setattr(instance, key, val)

        instance.save()
        return instance


def can_mutate_commodity(
    commodity: models.Commodity, update: bool = False, delete: bool = False
):
    shipment = models.Shipment.objects.filter(
        Q(customs__commodities__id=commodity.id) | Q(parcel__items__id=commodity.id)
    ).first()
    order = commodity.order.first() if settings.ORDERS_MANAGEMENT else None

    if shipment is None and order is None:
        return

    if update and shipment and shipment.status != ShipmentStatus.created.value:
        raise PurplshipAPIException(
            f"Operation not permitted. The related shipment is '{shipment.status}'.",
            status_code=status.HTTP_409_CONFLICT,
            code="state_error",
        )

    if delete and order and len(order.line_items.all()) == 1:
        raise PurplshipAPIException(
            f"Operation not permitted. The related order needs at least one line_item.",
            status_code=status.HTTP_409_CONFLICT,
            code="state_error",
        )
