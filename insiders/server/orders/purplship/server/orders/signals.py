import logging
from django.db.models import signals

from purplship.server.core.utils import failsafe
import purplship.server.orders.serializers as serializers
import purplship.server.manager.models as manager
from purplship.server.orders.serializers.order import compute_order_status
import purplship.server.orders.models as models
import purplship.server.events.tasks as tasks
from purplship.server.events.serializers import EventTypes

logger = logging.getLogger(__name__)


def register_signals():
    signals.post_save.connect(shipment_updated, sender=manager.Shipment)
    signals.post_save.connect(order_updated, sender=models.Order)

    logger.info("order webhooks signals registered...")


def shipment_updated(
    sender, instance, created, raw, using, update_fields, *args, **kwargs
):
    """Shipment related events:
    - shipment purchased (label purchased)
    - shipment fulfilled (shipped)
    """
    if not instance.shipment_order.exists():
        return

    if instance.status in [
        serializers.ShipmentStatus.purchased.value,
        serializers.ShipmentStatus.transit.value,
        serializers.ShipmentStatus.cancelled.value,
    ]:
        order = instance.shipment_order.first()
        status = compute_order_status(order)
        if status != order.status:
            order.status = status
            order.save(update_fields=["status"])
            logger.info("shipment's related order successfully updated")


def order_updated(
    sender, instance, created, raw, using, update_fields, *args, **kwargs
):
    """Order related events:
    - order created
    - order status changed (in-transit, delivered or blocked)
    """
    changes = update_fields or []

    if created:
        event = EventTypes.order_created.value
    elif "status" not in changes:
        return
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
    test_mode = instance.test_mode
    context = dict(
        user_id=failsafe(lambda: instance.created_by.id),
        org_id=getattr(getattr(instance, "org", None), "id", None),
    )

    tasks.notify_webhooks(event, data, event_at, context, test_mode)
