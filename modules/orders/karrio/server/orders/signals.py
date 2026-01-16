from rest_framework import status
from django.db.models import signals

from karrio.server.core import utils
from karrio.server.conf import settings
from karrio.server.core.utils import failsafe
from karrio.server.events.serializers import EventTypes
from karrio.server.orders.serializers.order import compute_order_status
from karrio.server.core.logging import logger
import karrio.server.orders.serializers as serializers
import karrio.server.manager.models as manager
import karrio.server.orders.models as models
import karrio.server.events.tasks as tasks
import karrio.server.core.exceptions as exceptions


def register_signals():
    signals.m2m_changed.connect(
        shipments_updated, sender=models.Order.shipments.through
    )
    signals.post_delete.connect(commodity_mutated, sender=manager.Commodity)
    signals.post_save.connect(commodity_mutated, sender=manager.Commodity)
    signals.post_save.connect(shipment_updated, sender=manager.Shipment)
    signals.post_save.connect(order_updated, sender=models.Order)

    logger.info("Signal registration complete", module="karrio.orders")


@utils.disable_for_loaddata
def commodity_mutated(sender, instance, *args, **kwargs):
    """Commodity mutations (added or removed)

    Note: With JSON-based order line_items and shipment parcels, the order-shipment
    linking is now handled through parent_id references in the JSON data rather than
    through M2M relations. This signal handler is kept for backward compatibility
    but primarily relies on the JSON-based shipment_updated handler for syncing.
    """
    # With JSON-based storage, order-shipment syncing is handled in shipment_updated
    # through _find_related_orders_from_json which checks parent_id links
    pass


def _find_related_orders_from_json(shipment_instance):
    """Find related orders by checking JSON parent_id links in parcel items.

    This handles the JSON-based approach where parcel items have parent_id
    linking to order line items stored in line_items.
    """
    parent_ids = set()

    # Collect all parent_ids from shipment's parcels
    parcels = shipment_instance.parcels or []
    for parcel in parcels:
        if not isinstance(parcel, dict):
            continue
        items = parcel.get("items") or []
        for item in items:
            if isinstance(item, dict) and item.get("parent_id"):
                parent_ids.add(item["parent_id"])

    if not parent_ids:
        return models.Order.objects.none()

    # Find orders that have line items with matching IDs
    # We need to query orders where any line_items[].id matches parent_ids
    related_orders = []
    for order in models.Order.objects.all():
        line_items = order.line_items or []
        for item in line_items:
            if isinstance(item, dict) and item.get("id") in parent_ids:
                related_orders.append(order.id)
                break

    return models.Order.objects.filter(id__in=related_orders)


def _update_order_line_items_fulfillment(order, shipment_instance):
    """Update order line_items unfulfilled_quantity based on shipment items.

    When a shipment is purchased/fulfilled, decrement the unfulfilled_quantity
    of the corresponding order line items.
    """
    if shipment_instance.status not in ["purchased", "transit", "delivered"]:
        return

    # Build a map of parent_id -> quantity from shipment items
    fulfilled_quantities = {}
    parcels = shipment_instance.parcels or []
    for parcel in parcels:
        if not isinstance(parcel, dict):
            continue
        items = parcel.get("items") or []
        for item in items:
            if isinstance(item, dict) and item.get("parent_id"):
                parent_id = item["parent_id"]
                quantity = item.get("quantity") or 1
                fulfilled_quantities[parent_id] = (
                    fulfilled_quantities.get(parent_id, 0) + quantity
                )

    if not fulfilled_quantities:
        return

    # Update order's line_items
    line_items = order.line_items or []
    updated = False
    for item in line_items:
        if not isinstance(item, dict):
            continue
        item_id = item.get("id")
        if item_id in fulfilled_quantities:
            quantity = item.get("quantity") or 1
            fulfilled = fulfilled_quantities[item_id]
            current_unfulfilled = item.get("unfulfilled_quantity", quantity)
            new_unfulfilled = max(0, current_unfulfilled - fulfilled)
            if item.get("unfulfilled_quantity") != new_unfulfilled:
                item["unfulfilled_quantity"] = new_unfulfilled
                updated = True

    if updated:
        order.line_items = line_items
        order.save(update_fields=["line_items"])


@utils.disable_for_loaddata
def shipment_updated(
    sender, instance, created, raw, using, update_fields, *args, **kwargs
):
    """Shipment related events:
    - shipment purchased (label purchased)
    - shipment fulfilled (shipped)
    """
    # Check if shipment has parcels with items linking to orders
    has_json_links = bool(instance.parcels)

    if not has_json_links:
        return

    # Retrieve all orders associated with this shipment using JSON-based lookup
    related_orders = _find_related_orders_from_json(instance)

    if related_orders.exists():
        meta = {
            **(instance.meta or {}),
            "orders": ",".join([_.id for _ in related_orders]),
        }
        manager.Shipment.objects.filter(id=instance.id).update(meta=meta)

    for order in related_orders:
        if order.shipments.filter(id=instance.id).exists() == False:
            order.shipments.add(instance)

        # Update line_items fulfillment tracking
        _update_order_line_items_fulfillment(order, instance)

        if instance.status != serializers.ShipmentStatus.draft.value:
            status = compute_order_status(order)
            if order.status != "cancelled" and status != order.status:
                order.status = status
                order.save(update_fields=["status"])
                logger.info("Order status updated from shipment", order_id=order.id, new_status=status)


@utils.disable_for_loaddata
def order_updated(sender, instance, *args, **kwargs):
    """Order related events:
    - order created
    - order status changed (in-transit, delivered or blocked)
    """
    created = kwargs.get("created", False)
    changes = kwargs.get("update_fields") or []
    post_create = created or "created_at" in changes

    # Clean up deduplication lock when order reaches a terminal state
    if not post_create and "status" in changes:
        terminal_statuses = [
            serializers.OrderStatus.cancelled.value,
            serializers.OrderStatus.delivered.value,
        ]
        if instance.status in terminal_statuses:
            models.OrderKey.objects.filter(order=instance).delete()

    if post_create:
        event = EventTypes.order_created.value
    elif "status" not in changes:
        event = EventTypes.order_updated.value
    elif instance.status == serializers.OrderStatus.fulfilled.value:
        event = EventTypes.order_fulfilled.value
    elif instance.status == serializers.OrderStatus.cancelled.value:
        event = EventTypes.order_cancelled.value
    elif instance.status == serializers.OrderStatus.delivered.value:
        event = EventTypes.order_delivered.value
    else:
        return

    data = serializers.Order(instance).data
    event_at = instance.updated_at
    context = dict(
        user_id=failsafe(lambda: instance.created_by.id),
        test_mode=instance.test_mode,
        org_id=failsafe(
            lambda: instance.org.first().id if hasattr(instance, "org") else None
        ),
    )

    if settings.MULTI_ORGANIZATIONS and context["org_id"] is None:
        return

    tasks.notify_webhooks(event, data, event_at, context, schema=settings.schema)


@utils.disable_for_loaddata
def shipments_updated(
    sender, instance, action, reverse, model, pk_set, *args, **kwargs
):
    """Order shipments updated"""

    status = compute_order_status(instance)
    if status != instance.status:
        instance.status = status
        instance.save(update_fields=["status"])
        logger.info("Order status updated from shipment", order_id=instance.id, new_status=status)
