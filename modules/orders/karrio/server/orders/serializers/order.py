from typing import Optional
from django.conf import settings
from django.apps import apps as django_apps
from django.db import transaction, IntegrityError
from rest_framework import status
from django.utils.functional import SimpleLazyObject

from karrio.server.core.exceptions import APIException
from karrio.server.serializers import (
    save_many_to_many_data,
    owned_model_serializer,
    save_one_to_one_data,
)
from karrio.server.core.logging import logger
import karrio.server.orders.serializers as serializers
import karrio.server.orders.models as models


class ScopeResolver:
    """Chain of responsibility for order scope resolution.

    Determines whether orders are scoped to an organization or user,
    supporting both multi-org and single-org deployments.
    """

    @staticmethod
    def from_context(context) -> str:
        """Resolve scope from request context.

        Returns:
            str: Scope identifier in format 'org:{id}' or 'user:{id}'

        Raises:
            APIException: If no authenticated user is found
        """
        user, org = ScopeResolver._extract_context(context)

        if scope_id := ScopeResolver._resolve_org_scope(org, user):
            return f"org:{scope_id}"

        if user_id := getattr(user, "id", None):
            return f"user:{user_id}"

        raise APIException(
            "An authenticated user is required to create orders.",
            code="user_required",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def _extract_context(context):
        """Extract user and org from various context types."""
        if isinstance(context, dict):
            user = context.get("user")
            org = context.get("org")
        else:
            user = getattr(context, "user", None)
            org = getattr(context, "org", None)

        # Unwrap lazy objects
        if isinstance(org, SimpleLazyObject):
            org = getattr(org, "_wrapped", None)

        return user, org

    @staticmethod
    def _resolve_org_scope(org, user) -> Optional[str]:
        """Try to resolve organization scope if multi-org is enabled."""
        if not (
            settings.MULTI_ORGANIZATIONS
            and django_apps.is_installed("karrio.server.orgs")
        ):
            return None

        # Try direct org first
        if org_id := getattr(org, "id", None):
            return org_id

        # Fallback to user's first active org
        user_id = getattr(user, "id", None)
        if user_id:
            try:
                import karrio.server.orgs.models as orgs

                org_obj = orgs.Organization.objects.filter(
                    users__id=user_id, is_active=True
                ).first()
                return getattr(org_obj, "id", None)
            except (ModuleNotFoundError, AttributeError):
                pass

        return None


# Backward compatibility alias
resolve_order_scope = ScopeResolver.from_context


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
        scope = ScopeResolver.from_context(context)
        source = validated_data.get("source") or "API"
        order_identifier = validated_data.get("order_id")

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

        # Acquire deduplication lock and create order
        with models.OrderKey.objects.acquire_lock(
            scope=scope,
            source=source,
            order_reference=order_identifier,
            test_mode=test_mode,
        ) as lock:
            order = models.Order.objects.create(**order_data)
            lock.bind_order(order)

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
