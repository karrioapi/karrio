"""
Management command to auto-close past pickups.

Replaces the Huey @db_periodic_task for use as a K8s CronJob:

    apiVersion: batch/v1
    kind: CronJob
    spec:
      schedule: "30 0 * * *"
      jobTemplate:
        spec:
          containers:
          - command: ["karrio", "close_pickups"]
"""

import logging

import karrio.server.core.utils as utils
from django.core.management.base import BaseCommand
from karrio.server.core.telemetry import with_task_telemetry

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Auto-close past one-time pickups across all tenants"

    @with_task_telemetry("close_pickups_command")
    def handle(self, *args, **options):
        from karrio.server.events.task_definitions.base import pickup

        self.stdout.write("Starting pickup auto-close...")

        @utils.run_on_all_tenants
        def _run(**kwargs):
            utils.failsafe(
                lambda: pickup.close_past_pickups(),
                "An error occurred during pickup auto-close: $error",
            )

        _run()

        self.stdout.write(self.style.SUCCESS("Pickup auto-close complete"))
