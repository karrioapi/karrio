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
@utils.error_wrapper
def shipment_updated(
    sender, instance, created, raw, using, update_fields, *args, **kwargs
):
    """Shipment related events:
    - shipment purchased (label purchased)
    - shipment fulfilled (shipped)
    """
    is_bound = "created_at" in (update_fields or [])
    status_updated = "status" in (update_fields or [])

    if created:
        return
    if is_bound and instance.status == serializers.ShipmentStatus.purchased.value:
        event = EventTypes.shipment_purchased.value
    elif (
        status_updated and instance.status == serializers.ShipmentStatus.purchased.value
    ):
        event = EventTypes.shipment_purchased.value
    elif (
        status_updated
        and instance.status == serializers.ShipmentStatus.in_transit.value
    ):
        event = EventTypes.shipment_fulfilled.value
    elif (
        status_updated and instance.status == serializers.ShipmentStatus.cancelled.value
    ):
        event = EventTypes.shipment_cancelled.value
    elif (
        status_updated
        and instance.status == serializers.ShipmentStatus.out_for_delivery.value
    ):
        event = EventTypes.shipment_out_for_delivery.value
    elif (
        status_updated
        and instance.status == serializers.ShipmentStatus.needs_attention.value
    ):
        event = EventTypes.shipment_needs_attention.value
    elif (
        status_updated
        and instance.status == serializers.ShipmentStatus.delivery_failed.value
    ):
        event = EventTypes.shipment_delivery_failed.value
    else:
        return

    data = serializers.Shipment(instance).data
    event_at = instance.updated_at
    context = dict(
        test_mode=instance.test_mode,
        user_id=utils.failsafe(lambda: instance.created_by.id),
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
    post_create = created or "created_at" in changes

    if post_create:
        event = EventTypes.tracker_created.value
    elif any(field in changes for field in ["status", "events"]):
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
