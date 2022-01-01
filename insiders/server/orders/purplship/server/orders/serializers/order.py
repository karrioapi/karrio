import logging
from typing import List
from django.db import transaction

from purplship.server.serializers import (
    owned_model_serializer,
    save_one_to_one_data,
)
from purplship.server.serializers.abstract import save_many_to_many_data
from purplship.server.orders.serializers import (
    OrderData,
    OrderStatus,
    ShipmentStatus,
    AddressSerializer,
    CommoditySerializer,
)
import purplship.server.orders.models as models

logger = logging.getLogger(__name__)


@owned_model_serializer
class OrderSerializer(OrderData):
    @transaction.atomic
    def create(self, validated_data: dict, context: dict, **kwargs) -> models.Order:
        mode_filter = validated_data.get("mode_filter") or {}
        test_mode = "test" in mode_filter and mode_filter.get("test") is not False

        order_data = {
            **{
                key: value
                for key, value in validated_data.items()
                if key in models.Order.DIRECT_PROPS and value is not None
            },
            "test_mode": test_mode,
            "shipping_address": save_one_to_one_data(
                "shipping_address",
                AddressSerializer,
                payload=validated_data,
                context=context,
            ),
        }

        order = models.Order.objects.create(**order_data)

        save_many_to_many_data(
            "line_items",
            CommoditySerializer,
            order,
            payload=validated_data,
            context=context,
        )

        return order

    @transaction.atomic
    def update(
        self, instance: models.Order, validated_data: dict, context: dict
    ) -> models.Order:
        changes = []
        data = validated_data.copy()

        for key, val in data.items():
            if key in models.Order.DIRECT_PROPS:
                setattr(instance, key, val)
                changes.append(key)
                validated_data.pop(key)

        status = compute_order_status(instance)
        if status != instance.status:
            instance.status = status
            changes.append("status")

        instance.save(update_fields=changes)

        return instance


def compute_order_status(order: models.Order) -> str:
    """
    Compute the order status based on the shipments and line_items statuses

    :param order: Order instance
    :return: Order status

    An order is considered to be "fulfilled" if all line_items are fulfilled (all quantities + shipments are purchased.)
    An order is considered to be "partially fulfilled" if some line_items are fulfilled and some are not.
    An order is considered to be "delivered" if all line_items are fulfilled and all shipments are delivered.

    The remaining statuses ("created", "cancelled") are self explanatory and should never be computed.
    """

    if not order.shipments.exclude(status=ShipmentStatus.cancelled.value).exists():
        return OrderStatus.created.value

    line_items_are_fulfilled = True
    line_items_are_partially_fulfilled = False
    shipments_are_delivered = all(
        [
            shipment.status == ShipmentStatus.delivered.value
            for shipment in order.shipments.all()
        ]
    )

    for line_item in order.line_items.all():
        shipment_items = line_item.children.exclude(
            parcels__shipment__status__in=[
                ShipmentStatus.cancelled.value,
                ShipmentStatus.created.value,
            ]
        )
        fulfilled = (
            sum([item.quantity for item in shipment_items]) >= line_item.quantity
        )

        if any(shipment_items) and fulfilled and not line_items_are_partially_fulfilled:
            line_items_are_partially_fulfilled = True

        if not fulfilled:
            line_items_are_fulfilled = False

    if line_items_are_fulfilled and shipments_are_delivered:
        return OrderStatus.delivered.value

    if line_items_are_fulfilled:
        return OrderStatus.fulfilled.value

    if line_items_are_partially_fulfilled:
        return OrderStatus.partially_fulfilled.value

    return OrderStatus.created.value


def shipment_has_order_line_items(order: models.Order, shipment_payload: dict):
    line_items_ids = [item.id for item in order.line_items.all()]
    shipment_parcel_items: List[dict] = sum(
        [parcel.get("items") or [] for parcel in shipment_payload.get("parcels")], []
    )

    return any(
        [item.get("parent_id") in line_items_ids for item in shipment_parcel_items]
    )
