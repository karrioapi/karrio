from typing import Optional
from django.conf import settings
from django.apps import apps as django_apps
from django.db import transaction, IntegrityError
from rest_framework import status
from django.utils.functional import SimpleLazyObject

from karrio.server.core.exceptions import APIException
from karrio.server.serializers import (
    owned_model_serializer,
    process_json_object_mutation,
    process_json_array_mutation,
)
import karrio.server.manager.models as manager_models
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


def process_order_line_items(payload: dict, instance=None):
    """Process line_items array for order create/update.

    Handles line item mutations and preserves fulfilled_quantity tracking.
    """
    if "line_items" not in payload:
        return getattr(instance, "line_items", None) if instance else []

    # Get existing items to preserve fulfilled_quantity
    existing_items = (instance.line_items or []) if instance else []
    existing_by_id = {
        item.get("id"): item
        for item in existing_items
        if isinstance(item, dict) and item.get("id")
    }

    result = process_json_array_mutation(
        "line_items", payload, instance,
        id_prefix="oli", model_class=manager_models.Commodity,
        data_field_name="line_items", object_type="commodity",
    )

    # Preserve fulfilled_quantity from existing items and initialize for new items
    if result:
        for item in result:
            item_id = item.get("id")
            if item_id and item_id in existing_by_id:
                existing = existing_by_id[item_id]
                if "fulfilled_quantity" not in item:
                    item["fulfilled_quantity"] = existing.get("fulfilled_quantity", 0)
            else:
                if "unfulfilled_quantity" not in item:
                    item["unfulfilled_quantity"] = item.get("quantity", 0)

    return result


@owned_model_serializer
class OrderSerializer(serializers.OrderData):
    @transaction.atomic
    def create(self, validated_data: dict, context: dict, **kwargs) -> models.Order:
        test_mode = getattr(context, "test_mode", False)
        scope = ScopeResolver.from_context(context)
        source = validated_data.get("source") or "API"
        order_identifier = validated_data.get("order_id")

        # Process JSON fields for addresses and line_items
        json_fields = {}

        if "shipping_to" in validated_data:
            json_fields.update(shipping_to=process_json_object_mutation(
                "shipping_to", validated_data, None,
                model_class=manager_models.Address, object_type="address", id_prefix="adr",
            ))

        if "shipping_from" in validated_data:
            json_fields.update(shipping_from=process_json_object_mutation(
                "shipping_from", validated_data, None,
                model_class=manager_models.Address, object_type="address", id_prefix="adr",
            ))

        if "billing_address" in validated_data:
            json_fields.update(billing_address=process_json_object_mutation(
                "billing_address", validated_data, None,
                model_class=manager_models.Address, object_type="address", id_prefix="adr",
            ))

        json_fields.update(line_items=process_order_line_items(validated_data))

        order_data = {
            **{
                key: value
                for key, value in validated_data.items()
                if key in models.Order.DIRECT_PROPS and value is not None
            },
            **json_fields,
            "test_mode": test_mode,
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

    # Use JSON field for line_items
    line_items = order.line_items or []
    for line_item in line_items:
        quantity = line_item.get("quantity", 1)
        unfulfilled_quantity = line_item.get("unfulfilled_quantity", quantity)
        fulfilled = unfulfilled_quantity <= 0
        partially_fulfilled = unfulfilled_quantity < quantity

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
