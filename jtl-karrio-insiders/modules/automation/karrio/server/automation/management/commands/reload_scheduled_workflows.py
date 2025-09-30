"""
Management command to reload all scheduled workflows.

This command clears all existing scheduled workflow registrations and
re-registers all active scheduled workflows from the database.
"""

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from karrio.server.automation.services.scheduler import workflow_scheduler
from karrio.server.automation.models import WorkflowTrigger
from karrio.server.automation.serializers import AutomationTriggerType


class Command(BaseCommand):
    help = 'Reload all scheduled workflows from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually doing it',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed output',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        verbose = options['verbose']

        self.stdout.write(
            self.style.SUCCESS('Reloading scheduled workflows...')
        )

        try:
            # Get current scheduled triggers
            scheduled_triggers = WorkflowTrigger.objects.filter(
                trigger_type=AutomationTriggerType.scheduled.value,
                workflow__is_active=True
            ).select_related('workflow')

            if verbose or dry_run:
                self.stdout.write(f"Found {scheduled_triggers.count()} scheduled workflow triggers:")
                for trigger in scheduled_triggers:
                    status = "✓ Active" if trigger.workflow.is_active else "✗ Inactive"
                    next_run = trigger.next_run_at.strftime('%Y-%m-%d %H:%M:%S') if trigger.next_run_at else "Not calculated"
                    self.stdout.write(
                        f"  - {trigger.workflow.name} ({trigger.schedule}) - {status} - Next: {next_run}"
                    )

            if not dry_run:
                # Reload scheduled workflows
                registered_count = workflow_scheduler.refresh_all_scheduled_workflows()

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully reloaded {registered_count} scheduled workflows'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING('Dry run - no changes made')
                )

        except Exception as e:
            raise CommandError(f'Failed to reload scheduled workflows: {e}')
