"""
Management command to run periodic data archiving.

Replaces the Huey @db_periodic_task for use as a K8s CronJob:

    apiVersion: batch/v1
    kind: CronJob
    spec:
      schedule: "0 0 * * *"
      jobTemplate:
        spec:
          containers:
          - command: ["karrio", "archive_data"]
"""

import logging

import karrio.server.core.utils as utils
from django.core.management.base import BaseCommand
from karrio.server.core.telemetry import with_task_telemetry

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run periodic data archiving across all tenants"

    @with_task_telemetry("archive_data_command")
    def handle(self, *args, **options):
        from karrio.server.events.task_definitions.base import archiving

        self.stdout.write("Starting periodic data archiving...")

        @utils.run_on_all_tenants
        def _run(**kwargs):
            utils.failsafe(
                lambda: archiving.run_data_archiving(),
                "An error occurred during data archiving: $error",
            )

        _run()

        self.stdout.write(self.style.SUCCESS("Data archiving complete"))
