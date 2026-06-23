"""
Management command to run the tracker update dispatcher.

Replaces the Huey @db_periodic_task for use as a K8s CronJob:

    apiVersion: batch/v1
    kind: CronJob
    spec:
      schedule: "0 */2 * * *"
      jobTemplate:
        spec:
          containers:
          - command: ["karrio", "update_trackers"]

Also usable for ad-hoc runs:

    karrio update_trackers
    karrio update_trackers --tracker-ids trk_abc123 trk_def456
"""

import logging

import karrio.server.core.utils as utils
from django.core.management.base import BaseCommand
from karrio.server.core.telemetry import with_task_telemetry

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run the tracker update dispatcher across all tenants"

    def add_arguments(self, parser):
        parser.add_argument(
            "--tracker-ids",
            nargs="*",
            default=None,
            help="Specific tracker IDs to update (default: all stale trackers)",
        )

    @with_task_telemetry("update_trackers_command")
    def handle(self, *args, **options):
        from karrio.server.events.task_definitions.base import tracking

        tracker_ids = options.get("tracker_ids")

        self.stdout.write("Starting tracker update dispatcher...")

        @utils.run_on_all_tenants
        def _run(**kwargs):
            tracking.update_trackers(
                tracker_ids=tracker_ids,
                schema=kwargs.get("schema"),
            )

        _run()

        self.stdout.write(self.style.SUCCESS("Tracker update complete"))
