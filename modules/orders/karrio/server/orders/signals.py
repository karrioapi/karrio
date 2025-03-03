import logging
from rest_framework import status
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
import karrio.server.core.exceptions as exceptions

logger = logging.getLogger(__name__)


def register_signals():
    signals.m2m_changed.connect(
        shipments_updated, sender=models.Order.shipments.through
    )
    signals.post_delete.connect(commodity_mutated, sender=manager.Commodity)
    signals.post_save.connect(commodity_mutated, sender=manager.Commodity)
    signals.post_save.connect(shipment_updated, sender=manager.Shipment)
    signals.post_save.connect(order_updated, sender=models.Order)

    logger.info("karrio.order signals registered...")


@utils.disable_for_loaddata
def commodity_mutated(sender, instance, *args, **kwargs):
    """Commodity mutations (added or removed)"""
    parent = utils.failsafe(lambda: instance.parent)

    if parent is None or parent.order is None:
        return

    order_shipments = manager.Shipment.objects.filter(
        parcels__items__parent_id__in=parent.order.line_items.values_list(
            "id", flat=True
        )
    ).distinct()

    for shipment in order_shipments:
        if parent.order.shipments.filter(id=shipment.id).exists() == False:
            parent.order.shipments.add(shipment)

    for shipment in parent.order.shipments.all():
        if order_shipments.filter(id=shipment.id).exists() == False:
            parent.order.shipments.remove(shipment)


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

    # Retrieve all orders associated with this shipment and update their status if needed
    related_orders = models.Order.objects.filter(
        line_items__children__commodity_parcel__parcel_shipment__id=instance.id
    ).distinct()

    if related_orders.exists():
        meta = {
            **(instance.meta or {}),
            "orders": ",".join([_.id for _ in related_orders]),
        }
        manager.Shipment.objects.filter(id=instance.id).update(meta=meta)

    for order in related_orders:
        if order.shipments.filter(id=instance.id).exists() == False:
            order.shipments.add(instance)

        if instance.status != serializers.ShipmentStatus.draft.value:
            status = compute_order_status(order)
            if order.status != "cancelled" and status != order.status:
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
    post_create = created or "created_at" in changes

    if post_create:
        duplicates = (
            models.Order.access_by(instance.created_by)
            .exclude(status="cancelled")
            .filter(
                source=instance.source,
                order_id=instance.order_id,
                test_mode=instance.test_mode,
            )
            .count()
        )

        if duplicates > 1:
            raise exceptions.APIException(
                detail=f"An order with 'order_id' {instance.order_id} from {instance.source} already exists.",
                status_code=status.HTTP_409_CONFLICT,
            )

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
        logger.info("shipment related order successfully updated")
