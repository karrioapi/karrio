import logging
from django.db import transaction
from rest_framework import status

from karrio.server.core.exceptions import APIException
from karrio.server.serializers import (
    save_many_to_many_data,
    owned_model_serializer,
    save_one_to_one_data,
)
import karrio.server.orders.serializers as serializers
import karrio.server.orders.models as models

logger = logging.getLogger(__name__)


@owned_model_serializer
class LineItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LineItem
        exclude = ["created_at", "updated_at", "created_by"]


@owned_model_serializer
class OrderSerializer(serializers.OrderData):
    @transaction.atomic
    def create(self, validated_data: dict, context: dict, **kwargs) -> models.Order:
        test_mode = getattr(context, "test_mode", False)

        order_data = {
            **{
                key: value
                for key, value in validated_data.items()
                if key in models.Order.DIRECT_PROPS and value is not None
            },
            "test_mode": test_mode,
            "shipping_to": save_one_to_one_data(
                "shipping_to",
                serializers.AddressSerializer,
                payload=validated_data,
                context=context,
            ),
            "shipping_from": save_one_to_one_data(
                "shipping_from",
                serializers.AddressSerializer,
                payload=validated_data,
                context=context,
            ),
            "billing_address": save_one_to_one_data(
                "billing_address",
                serializers.AddressSerializer,
                payload=validated_data,
                context=context,
            ),
        }

        order = models.Order.objects.create(**order_data)

        save_many_to_many_data(
            "line_items",
            LineItemModelSerializer,
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


class OrderUpdateData(serializers.Serializer):
    options = serializers.PlainDictField(
        required=False,
        allow_null=True,
        help_text="""<details>
        <summary>The options available for the order shipments.</summary>

        {
            "currency": "USD",
            "paid_by": "third_party",
            "payment_account_number": "123456789",
            "duty_paid_by": "recipient",
            "duty_account_number": "123456789",
            "invoice_number": "123456789",
            "invoice_date": "2020-01-01",
            "single_item_per_parcel": true,
            "carrier_ids": ["canadapost-test"],
        }
        </details>
        """,
    )
    metadata = serializers.PlainDictField(
        required=False, help_text="User metadata for the shipment"
    )


def compute_order_status(order: models.Order) -> str:
    """
    Compute the order status based on the shipments and line_items statuses

    :param order: Order instance
    :return: Order status

    An order is considered to be "fulfilled" if all line_items are fulfilled (all quantities + shipments are purchased.)
    An order is considered to be "partially fulfilled" if some line_items are fulfilled and some are not.
    An order is considered to be "delivered" if all line_items are fulfilled and all shipments are delivered.

    The remaining statuses ("unfulfilled", "cancelled") are self explanatory and should never be computed.
    """

    if not order.shipments.exclude(status="cancelled").exists():
        return serializers.OrderStatus.unfulfilled.value

    line_items_are_fulfilled = True
    line_items_are_partially_fulfilled = False
    shipments_are_delivered = all(
        [
            shipment.status == serializers.ShipmentStatus.delivered.value
            for shipment in order.shipments.all()
        ]
    )

    for line_item in order.line_items.all():
        fulfilled = line_item.unfulfilled_quantity <= 0
        partially_fulfilled = line_item.unfulfilled_quantity < line_item.quantity

        if partially_fulfilled and not line_items_are_partially_fulfilled:
            line_items_are_partially_fulfilled = True

        if not fulfilled:
            line_items_are_fulfilled = False

    if line_items_are_fulfilled and shipments_are_delivered:
        return serializers.OrderStatus.delivered.value

    if line_items_are_fulfilled:
        return serializers.OrderStatus.fulfilled.value

    if line_items_are_partially_fulfilled:
        return serializers.OrderStatus.partial.value

    return serializers.OrderStatus.unfulfilled.value


def can_mutate_order(
    order: models.Order,
    update: bool = False,
    delete: bool = False,
    payload: dict = None,
):
    if update and [*(payload or {}).keys()] == ["metadata"]:
        return

    if update and order.status in [
        serializers.OrderStatus.delivered.value,
        serializers.OrderStatus.fulfilled.value,
    ]:
        raise APIException(
            f"The order is '{order.status}' and cannot be updated anymore...",
            code="state_error",
            status_code=status.HTTP_409_CONFLICT,
        )

    if delete and order.status in [
        serializers.OrderStatus.delivered.value,
        serializers.OrderStatus.cancelled.value,
    ]:
        raise APIException(
            f"The order is '{order.status}' and can not be cancelled anymore...",
            code="state_error",
            status_code=status.HTTP_409_CONFLICT,
        )

    if delete and order.status in [
        serializers.OrderStatus.fulfilled.value,
        serializers.OrderStatus.partial.value,
    ]:
        raise APIException(
            f"The order is '{order.status}' please cancel all related shipments before...",
            code="state_error",
            status_code=status.HTTP_409_CONFLICT,
        )
