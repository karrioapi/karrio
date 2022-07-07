import logging
from django.db.models import signals

from karrio.server.core import utils
from karrio.server.conf import settings
from karrio.server.events.serializers import EventTypes
import karrio.server.core.serializers as serializers
import karrio.server.manager.models as models
import karrio.server.events.tasks as tasks

logger = logging.getLogger(__name__)


def register_signals():
    signals.post_save.connect(shipment_updated, sender=models.Shipment)
    signals.post_delete.connect(shipment_cancelled, sender=models.Shipment)
    signals.post_save.connect(tracker_updated, sender=models.Tracking)

    logger.info("karrio.events signals registered...")


@utils.disable_for_loaddata
def shipment_updated(
    sender, instance, created, raw, using, update_fields, *args, **kwargs
):
    """Shipment related events:
    - shipment purchased (label purchased)
    - shipment fulfilled (shipped)
    """
    if created and instance.status != serializers.ShipmentStatus.purchased.value:
        return
    elif instance.status == serializers.ShipmentStatus.purchased.value:
        event = EventTypes.shipment_purchased.value
    elif instance.status == serializers.ShipmentStatus.in_transit.value:
        event = EventTypes.shipment_fulfilled.value
    elif instance.status == serializers.ShipmentStatus.cancelled.value:
        event = EventTypes.shipment_cancelled.value
    else:
        return

    data = serializers.Shipment(instance).data
    event_at = instance.updated_at
    context = dict(
        user_id=utils.failsafe(lambda: instance.created_by.id),
        test_mode=instance.test_mode,
        org_id=utils.failsafe(
            lambda: instance.org.first().id if hasattr(instance, "org") else None
        ),
    )

    if settings.MULTI_ORGANIZATIONS and context["org_id"] is None:
        return

    tasks.notify_webhooks(event, data, event_at, context, schema=settings.schema)


@utils.disable_for_loaddata
def shipment_cancelled(sender, instance, *args, **kwargs):
    """Shipment related events:
    - shipment cancelled/deleted (label voided)
    """
    event = EventTypes.shipment_cancelled.value
    data = serializers.Shipment(instance)
    event_at = instance.updated_at
    context = dict(
        user_id=utils.failsafe(lambda: instance.created_by.id),
        test_mode=instance.test_mode,
        org_id=utils.failsafe(
            lambda: instance.org.first().id if hasattr(instance, "org") else None
        ),
    )

    if settings.MULTI_ORGANIZATIONS and context["org_id"] is None:
        return

    tasks.notify_webhooks(event, data, event_at, context, schema=settings.schema)


@utils.disable_for_loaddata
def tracker_updated(
    sender, instance, created, raw, using, update_fields, *args, **kwargs
):
    """Tracking related events:
    - tracker created (pending)
    - tracker status changed (in_transit, delivered or blocked)
    """
    changes = update_fields or []

    if created or "created_at" in changes:
        event = EventTypes.tracker_created.value
    elif any(field in changes for field in ["status"]):
        event = EventTypes.tracker_updated.value
    else:
        return

    data = serializers.TrackingStatus(instance).data
    event_at = instance.updated_at
    context = dict(
        user_id=utils.failsafe(lambda: instance.created_by.id),
        test_mode=instance.test_mode,
        org_id=utils.failsafe(
            lambda: instance.org.first().id if hasattr(instance, "org") else None
        ),
    )

    if settings.MULTI_ORGANIZATIONS and context["org_id"] is None:
        return

    tasks.notify_webhooks(event, data, event_at, context, schema=settings.schema)
