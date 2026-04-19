"""
Management command to dispatch due scheduled workflows.

Replaces the dynamic Huey @periodic_task registration for use as a K8s CronJob:

    apiVersion: batch/v1
    kind: CronJob
    spec:
      schedule: "* * * * *"    # every minute
      jobTemplate:
        spec:
          containers:
          - command: ["karrio", "dispatch_scheduled_workflows"]

Polls WorkflowTrigger records where next_run_at <= now and dispatches
them via the task backend. 1-minute granularity is sufficient for most
scheduled workflows (hourly/daily).
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from karrio.server.core.logging import logger


class Command(BaseCommand):
    help = "Dispatch due scheduled workflow triggers"

    def handle(self, *args, **options):
        try:
            from karrio.server.automation import models
            from karrio.server.automation.tasks import execute_scheduled_workflow
        except ImportError:
            self.stdout.write("Automation module not installed, skipping")
            return

        now = timezone.now()

        due_triggers = models.WorkflowTrigger.objects.select_related("workflow").filter(
            next_run_at__lte=now,
            workflow__is_active=True,
        )

        count = 0
        for trigger in due_triggers:
            try:
                execute_scheduled_workflow(trigger.id)
                count += 1
                logger.info(
                    "Dispatched scheduled workflow",
                    trigger_id=trigger.id,
                    workflow_id=trigger.workflow_id,
                )
            except Exception as e:
                logger.error(
                    "Failed to dispatch scheduled workflow",
                    trigger_id=trigger.id,
                    error=str(e),
                )

        self.stdout.write(self.style.SUCCESS(f"Dispatched {count} scheduled workflow(s)"))
