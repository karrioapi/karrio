import logging
from django.db.models import signals

from karrio.server.conf import settings
import karrio.server.core.utils as utils
import karrio.server.data.models as models
import karrio.server.events.tasks as tasks
import karrio.server.data.serializers as serializers

logger = logging.getLogger(__name__)


def register_all():
    signals.post_save.connect(batch_operation_updated, sender=models.BatchOperation)

    logger.info("karrio.data signals registered...")


@utils.disable_for_loaddata
def batch_operation_updated(sender, instance, *args, **kwargs):
    """Process batch related events
    - Create event on batch creation and completion
    - Notifiy webhook subscribers of batch operation updates
    """
    changes = kwargs.get("update_fields") or []
    post_create = "created_at" in changes

    if post_create:
        event = serializers.EventTypes.batch_queued.value
    elif instance.status == serializers.BatchOperationStatus.running.value:
        event = serializers.EventTypes.batch_running.value
        # Run post creation processing for batch_operation resources
        tasks.process_batch_resources(instance.id, schema=settings.schema)
    elif instance.status == serializers.BatchOperationStatus.completed.value:
        event = serializers.EventTypes.batch_completed.value
    else:
        return

    data = serializers.BatchOperation(instance).data
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
