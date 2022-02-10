import logging
from django.db.models import signals

from purplship.server.conf import settings
from purplship.server.core.utils import failsafe
import purplship.server.core.serializers as serializers
import purplship.server.manager.models as models
import purplship.server.events.tasks as tasks
from purplship.server.events.serializers import EventTypes

logger = logging.getLogger(__name__)


def register_signals():
    signals.post_save.connect(shipment_updated, sender=models.Shipment)
    signals.post_delete.connect(shipment_cancelled, sender=models.Shipment)
    signals.post_save.connect(tracker_updated, sender=models.Tracking)

    logger.info("webhooks signals registered...")


def shipment_updated(
    sender, instance, created, raw, using, update_fields, *args, **kwargs
):
    """Shipment related events:
    - shipment purchased (label purchased)
    - shipment fulfilled (shipped)
    """
    changes = update_fields or {}

    if created or "status" not in changes:
        return
    elif instance.status == serializers.ShipmentStatus.purchased.value:
        event = EventTypes.shipment_purchased.value
    elif instance.status == serializers.ShipmentStatus.transit.value:
        event = EventTypes.shipment_fulfilled.value
    elif instance.status == serializers.ShipmentStatus.cancelled.value:
        event = EventTypes.shipment_cancelled.value
    else:
        return

    data = serializers.Shipment(instance).data
    event_at = instance.updated_at
    test_mode = instance.test_mode
    context = dict(
        user_id=failsafe(lambda: instance.created_by.id),
        org_id=failsafe(
            lambda: instance.org.first().id if hasattr(instance, "org") else None
        ),
    )

    if settings.MULTI_ORGANIZATIONS and context["org_id"] is None:
        return

    tasks.notify_webhooks(
        event, data, event_at, context, test_mode, schema=settings.schema
    )


def shipment_cancelled(sender, instance, *args, **kwargs):
    """Shipment related events:
    - shipment cancelled/deleted (label voided)
    """
    event = EventTypes.shipment_cancelled.value
    data = serializers.Shipment(instance)
    event_at = instance.updated_at
    test_mode = instance.test_mode
    context = dict(
        user_id=failsafe(lambda: instance.created_by.id),
        org_id=failsafe(
            lambda: instance.org.first().id if hasattr(instance, "org") else None
        ),
    )

    if settings.MULTI_ORGANIZATIONS and context["org_id"] is None:
        return

    tasks.notify_webhooks(
        event, data, event_at, context, test_mode, schema=settings.schema
    )


def tracker_updated(
    sender, instance, created, raw, using, update_fields, *args, **kwargs
):
    """Tracking related events:
    - tracker created (pending)
    - tracker status changed (in-transit, delivered or blocked)
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
    test_mode = instance.test_mode
    context = dict(
        user_id=failsafe(lambda: instance.created_by.id),
        org_id=failsafe(
            lambda: instance.org.first().id if hasattr(instance, "org") else None
        ),
    )

    if settings.MULTI_ORGANIZATIONS and context["org_id"] is None:
        return

    tasks.notify_webhooks(
        event, data, event_at, context, test_mode, schema=settings.schema
    )
