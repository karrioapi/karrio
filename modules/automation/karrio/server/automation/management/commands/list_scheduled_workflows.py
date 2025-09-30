"""
Management command to list all scheduled workflows.

This command shows all scheduled workflow triggers and their status.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone

from karrio.server.automation.services.scheduler import workflow_scheduler
from karrio.server.automation.models import WorkflowTrigger
from karrio.server.automation.serializers import AutomationTriggerType
from karrio.server.automation.cron_utils import get_cron_description


class Command(BaseCommand):
    help = 'List all scheduled workflows'

    def add_arguments(self, parser):
        parser.add_argument(
            '--show-inactive',
            action='store_true',
            help='Include inactive workflows in the listing',
        )
        parser.add_argument(
            '--show-registered',
            action='store_true',
            help='Show which workflows are currently registered with the scheduler',
        )

    def handle(self, *args, **options):
        show_inactive = options['show_inactive']
        show_registered = options['show_registered']

        self.stdout.write(
            self.style.SUCCESS('Scheduled Workflows:')
        )
        self.stdout.write('=' * 80)

        # Build query
        query = WorkflowTrigger.objects.filter(
            trigger_type=AutomationTriggerType.scheduled.value
        ).select_related('workflow')

        if not show_inactive:
            query = query.filter(workflow__is_active=True)

        scheduled_triggers = query.order_by('workflow__name')

        if not scheduled_triggers.exists():
            self.stdout.write(
                self.style.WARNING('No scheduled workflows found.')
            )
            return

        now = timezone.now()

        for trigger in scheduled_triggers:
            # Workflow status
            if trigger.workflow.is_active:
                status_icon = "✓"
                status_color = self.style.SUCCESS
            else:
                status_icon = "✗"
                status_color = self.style.ERROR

            # Registration status
            registered_status = ""
            if show_registered:
                is_registered = workflow_scheduler.is_registered(trigger.id)
                registered_status = " [REGISTERED]" if is_registered else " [NOT REGISTERED]"

            # Next run information
            if trigger.next_run_at:
                if trigger.next_run_at <= now:
                    next_run_info = self.style.WARNING(f"DUE NOW ({trigger.next_run_at.strftime('%Y-%m-%d %H:%M:%S')})")
                else:
                    time_until = trigger.next_run_at - now
                    if time_until.days > 0:
                        next_run_info = f"in {time_until.days} days ({trigger.next_run_at.strftime('%Y-%m-%d %H:%M:%S')})"
                    else:
                        hours = time_until.seconds // 3600
                        minutes = (time_until.seconds % 3600) // 60
                        next_run_info = f"in {hours}h {minutes}m ({trigger.next_run_at.strftime('%H:%M:%S')})"
            else:
                next_run_info = self.style.WARNING("Not calculated")

            # Last run information
            if trigger.last_run_at:
                time_since = now - trigger.last_run_at
                if time_since.days > 0:
                    last_run_info = f"{time_since.days} days ago"
                else:
                    hours = time_since.seconds // 3600
                    minutes = (time_since.seconds % 3600) // 60
                    last_run_info = f"{hours}h {minutes}m ago"
            else:
                last_run_info = "Never"

            # Schedule description
            try:
                schedule_desc = get_cron_description(trigger.schedule)
            except:
                schedule_desc = trigger.schedule

            # Output workflow information
            self.stdout.write(
                status_color(f"{status_icon} {trigger.workflow.name}{registered_status}")
            )
            self.stdout.write(f"   ID: {trigger.workflow.id}")
            self.stdout.write(f"   Schedule: {trigger.schedule} ({schedule_desc})")
            self.stdout.write(f"   Next run: {next_run_info}")
            self.stdout.write(f"   Last run: {last_run_info}")

            if trigger.workflow.description:
                self.stdout.write(f"   Description: {trigger.workflow.description}")

            self.stdout.write("")  # Empty line for spacing

        # Summary
        total_count = scheduled_triggers.count()
        active_count = scheduled_triggers.filter(workflow__is_active=True).count()

        if show_registered:
            registered_count = workflow_scheduler.get_registered_count()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Total: {total_count} scheduled workflows "
                    f"({active_count} active, {registered_count} registered)"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Total: {total_count} scheduled workflows ({active_count} active)"
                )
            )
