import logging
from django.db.models import signals

from karrio.server.core import utils
from karrio.server.conf import settings
from karrio.server.core.utils import failsafe
from karrio.server.events.serializers import EventTypes
from karrio.server.orders.serializers.order import compute_order_status
import karrio.server.orders.serializers as serializers
import karrio.server.manager.models as manager
import karrio.server.orders.models as models
import karrio.server.events.tasks as tasks

logger = logging.getLogger(__name__)


def register_signals():
    signals.post_delete.connect(commodity_mutated, sender=manager.Commodity)
    signals.post_save.connect(commodity_mutated, sender=manager.Commodity)
    signals.post_save.connect(shipment_updated, sender=manager.Shipment)
    signals.post_save.connect(order_updated, sender=models.Order)

    logger.info("karrio.order signals registered...")


@utils.disable_for_loaddata
def commodity_mutated(sender, instance, *args, **kwargs):
    """Commodity mutations (added or removed)"""

    try:
        parent = getattr(instance, "parent", None)
    except Exception as e:
        return

    if parent is None:
        return

    if parent.order is None:
        return

    # Retrieve all orders associated with this commodity and update their status if needed
    for order in models.Order.objects.filter(
        line_items__id=instance.parent_id
    ).distinct():
        status = compute_order_status(order)
        if status != order.status:
            order.status = status
            order.save(update_fields=["status"])
            logger.info("commodity related order successfully updated")


@utils.disable_for_loaddata
def shipment_updated(
    sender, instance, created, raw, using, update_fields, *args, **kwargs
):
    """Shipment related events:
    - shipment purchased (label purchased)
    - shipment fulfilled (shipped)
    """
    if not instance.parcels.filter(
        items__parent__order_link__order__isnull=False
    ).exists():
        return

    if instance.status != serializers.ShipmentStatus.draft.value:
        # Retrieve all orders associated with this shipment and update their status if needed
        for order in models.Order.objects.filter(
            line_items__children__commodity_parcel__parcel_shipment__id=instance.id
        ).distinct():
            status = compute_order_status(order)
            if status != order.status:
                order.status = status
                order.save(update_fields=["status"])
                logger.info("shipment related order successfully updated")


@utils.disable_for_loaddata
def order_updated(sender, instance, *args, **kwargs):
    """Order related events:
    - order created
    - order status changed (in-transit, delivered or blocked)
    """
    created = kwargs.get("created", False)
    changes = kwargs.get("update_fields") or []

    if "created_at" in changes:
        duplicates = (
            models.Order.objects.exclude(status="cancelled")
            .filter(
                org=instance.link.org,
                source=instance.source,
                order_id=instance.order_id,
                test_mode=instance.test_mode,
            )
            .count()
        )

        if duplicates > 1:
            raise serializers.ValidationError(
                {
                    "order_id": f"An order with 'order_id' {instance.order_id} already exists."
                }
            )

    if created or "created_at" in changes:
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
