import logging
from django.db.models import signals

import purpleserver.core.serializers as serializers
import purpleserver.manager.models as models
import purpleserver.events.tasks as tasks
from purpleserver.events.serializers import EventTypes

logger = logging.getLogger(__name__)


def register_signals():
    signals.post_save.connect(shipment_updated, sender=models.Shipment)
    signals.post_delete.connect(shipment_cancelled, sender=models.Shipment)
    signals.post_save.connect(tracker_updated, sender=models.Tracking)

    logger.info("webhooks signals registered...")


def shipment_updated(sender, instance, created, raw, using, update_fields, *args, **kwargs):
    """Shipment related events:
        - shipment purchased (label purchased)
        - shipment fulfilled (shipped)
    """
    changes = update_fields or {}

    if created or 'status' not in changes:
        return
    elif instance.status == serializers.ShipmentStatus.purchased.value:
        event = EventTypes.shipment_purchased.value
    elif instance.status == serializers.ShipmentStatus.transit.value:
        event = EventTypes.shipment_fulfilled.value
    else:
        return

    data = serializers.Shipment(instance).data
    event_at = instance.updated_at
    test_mode = instance.test_mode

    tasks.notify_webhooks(event, data, event_at, test_mode)


def shipment_cancelled(sender, instance, *args, **kwargs):
    """Shipment related events:
        - shipment cancelled/deleted (label voided)
    """
    event = EventTypes.shipment_cancelled.value
    data = serializers.Shipment(instance)
    event_at = instance.updated_at
    test_mode = instance.test_mode

    tasks.notify_webhooks(event, data, event_at, test_mode)


def tracker_updated(sender, instance, created, raw, using, update_fields, *args, **kwargs):
    """Tracking related events:
        - tracker created (in-transit)
        - tracker status changed (delivered or blocked)
    """
    if created:
        event = EventTypes.tracker_created.value
    elif any(field in update_fields for field in ['delivered', 'events']):
        event = EventTypes.tracker_updated.value
    else:
        return

    data = serializers.TrackingStatus(instance).data
    event_at = instance.updated_at
    test_mode = instance.test_mode

    tasks.notify_webhooks(event, data, event_at, test_mode)
