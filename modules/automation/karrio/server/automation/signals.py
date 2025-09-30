import logging
import django.db.models.signals as signals

import karrio.server.core.utils as utils
import karrio.server.events.tasks as tasks
import karrio.server.automation.models as models
import karrio.server.automation.serializers as automation_serializers

logger = logging.getLogger(__name__)


def register():
    signals.post_save.connect(event_updated, sender=models.WorkflowEvent)
    signals.post_save.connect(workflow_trigger_saved, sender=models.WorkflowTrigger)
    signals.post_delete.connect(workflow_trigger_deleted, sender=models.WorkflowTrigger)

    logger.info("karrio.automation signals registered...")


@utils.disable_for_loaddata
@utils.error_wrapper
def event_updated(
    sender, instance, created, raw, using, update_fields, *args, **kwargs
):
    """Background signal for workflow background execution."""
    is_bound = "created_at" in (update_fields or [])

    if created:
        return
    if (
        not is_bound
        and instance.status
        != automation_serializers.AutomationEventStatus.pending.value
    ):
        return

    if instance.status in [
        automation_serializers.AutomationEventStatus.pending.value,
    ]:
        print("queueing workflow event...", instance.id, instance.status)
        tasks.queue_workflow_event(instance.id)


@utils.disable_for_loaddata
@utils.error_wrapper
def workflow_trigger_saved(
    sender, instance, created, raw, using, update_fields, *args, **kwargs
):
    """Handle workflow trigger creation and updates for scheduled triggers."""
    # Only process scheduled triggers
    if instance.trigger_type != automation_serializers.AutomationTriggerType.scheduled.value:
        return

    # Skip during data loading
    if raw:
        return

    try:
        from karrio.server.automation.services.scheduler import workflow_scheduler

        if created:
            # Register new scheduled workflow
            logger.info(f"Registering new scheduled workflow trigger {instance.id}")
            workflow_scheduler.register_scheduled_workflow(instance)
        else:
            # Re-register updated scheduled workflow (unregister then register)
            logger.info(f"Re-registering updated scheduled workflow trigger {instance.id}")
            workflow_scheduler.unregister_scheduled_workflow(instance)
            workflow_scheduler.register_scheduled_workflow(instance)

    except Exception as e:
        logger.error(f"Failed to handle scheduled workflow trigger {instance.id}: {e}")


@utils.disable_for_loaddata
@utils.error_wrapper
def workflow_trigger_deleted(sender, instance, using, *args, **kwargs):
    """Handle workflow trigger deletion for scheduled triggers."""
    # Only process scheduled triggers
    if instance.trigger_type != automation_serializers.AutomationTriggerType.scheduled.value:
        return

    try:
        from karrio.server.automation.services.scheduler import workflow_scheduler

        logger.info(f"Unregistering deleted scheduled workflow trigger {instance.id}")
        workflow_scheduler.unregister_scheduled_workflow(instance)

    except Exception as e:
        logger.error(f"Failed to unregister deleted workflow trigger {instance.id}: {e}")
