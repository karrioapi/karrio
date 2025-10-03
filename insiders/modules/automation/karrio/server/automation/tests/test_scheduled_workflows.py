import datetime
from unittest.mock import Mock, patch, MagicMock
from django.test import TestCase, override_settings
from django.utils import timezone
from django.core.exceptions import ValidationError

from karrio.server.automation.models import Workflow, WorkflowTrigger, WorkflowEvent
from karrio.server.automation.serializers import AutomationTriggerType, AutomationEventType
from karrio.server.automation.services.scheduler import WorkflowScheduler, ScheduledWorkflowRegistry
from karrio.server.automation.exceptions import InvalidCronExpressionError


class TestWorkflowScheduler(TestCase):
    """Test the WorkflowScheduler service"""

    def setUp(self):
        # Clear any existing registrations
        ScheduledWorkflowRegistry.clear()

        self.workflow = Workflow.objects.create(
            name="Test Scheduled Workflow",
            slug="test-scheduled-workflow",
            is_active=True,
        )

        self.scheduler = WorkflowScheduler()

    def test_register_scheduled_workflow_valid_cron(self):
        """Test registering a workflow with valid cron expression"""
        trigger = WorkflowTrigger.objects.create(
            slug="test-trigger",
            workflow=self.workflow,
            trigger_type=AutomationTriggerType.scheduled.value,
            schedule="0 9 * * 1",  # Every Monday at 9 AM
        )

        # Should successfully register without exceptions
        task_function = self.scheduler.register_scheduled_workflow(trigger)

        # Verify task function was created
        self.assertIsNotNone(task_function)
        self.assertTrue(callable(task_function))

        # Verify trigger is in registry
        self.assertIn(trigger.id, ScheduledWorkflowRegistry.get_registered_triggers())

    def test_register_scheduled_workflow_invalid_cron(self):
        """Test registering a workflow with invalid cron expression"""
        trigger = WorkflowTrigger.objects.create(
            slug="test-invalid-trigger",
            workflow=self.workflow,
            trigger_type=AutomationTriggerType.scheduled.value,
            schedule="invalid cron",
        )

        # Should raise InvalidCronExpressionError
        with self.assertRaises(InvalidCronExpressionError):
            self.scheduler.register_scheduled_workflow(trigger)

    def test_unregister_scheduled_workflow(self):
        """Test unregistering a scheduled workflow"""
        trigger = WorkflowTrigger.objects.create(
            slug="test-unregister-trigger",
            workflow=self.workflow,
            trigger_type=AutomationTriggerType.scheduled.value,
            schedule="0 9 * * 1",
        )

        # Register first
        self.scheduler.register_scheduled_workflow(trigger)
        self.assertIn(trigger.id, ScheduledWorkflowRegistry.get_registered_triggers())

        # Unregister
        self.scheduler.unregister_scheduled_workflow(trigger)
        self.assertNotIn(trigger.id, ScheduledWorkflowRegistry.get_registered_triggers())

    def test_refresh_all_scheduled_workflows(self):
        """Test refreshing all scheduled workflows from database"""
        # Create multiple scheduled triggers
        triggers = []
        for i in range(3):
            trigger = WorkflowTrigger.objects.create(
                slug=f"test-refresh-trigger-{i}",
                workflow=Workflow.objects.create(
                    name=f"Test Workflow {i}",
                    slug=f"test-workflow-{i}",
                    is_active=True,
                ),
                trigger_type=AutomationTriggerType.scheduled.value,
                schedule="0 9 * * 1",
            )
            triggers.append(trigger)

        # Refresh should register all active scheduled workflows
        registered_count = self.scheduler.refresh_all_scheduled_workflows()

        self.assertEqual(registered_count, 3)
        for trigger in triggers:
            self.assertIn(trigger.id, ScheduledWorkflowRegistry.get_registered_triggers())

    def test_refresh_ignores_inactive_workflows(self):
        """Test that refresh ignores workflows that are not active"""
        # Create inactive workflow
        inactive_workflow = Workflow.objects.create(
            name="Inactive Workflow",
            slug="inactive-workflow",
            is_active=False,
        )

        WorkflowTrigger.objects.create(
            slug="inactive-trigger",
            workflow=inactive_workflow,
            trigger_type=AutomationTriggerType.scheduled.value,
            schedule="0 9 * * 1",
        )

        # Refresh should not register inactive workflows
        registered_count = self.scheduler.refresh_all_scheduled_workflows()

        self.assertEqual(registered_count, 0)


class TestWorkflowTriggerModel(TestCase):
    """Test enhancements to WorkflowTrigger model for scheduled workflows"""

    def setUp(self):
        self.workflow = Workflow.objects.create(
            name="Test Workflow",
            slug="test-workflow",
            is_active=True,
        )

    def test_clean_valid_cron_expression(self):
        """Test model validation with valid cron expression"""
        trigger = WorkflowTrigger(
            slug="test-trigger",
            workflow=self.workflow,
            trigger_type=AutomationTriggerType.scheduled.value,
            schedule="0 9 * * 1",  # Every Monday at 9 AM
        )

        # Should not raise ValidationError
        trigger.clean()

    def test_clean_invalid_cron_expression(self):
        """Test model validation with invalid cron expression"""
        trigger = WorkflowTrigger(
            slug="test-trigger",
            workflow=self.workflow,
            trigger_type=AutomationTriggerType.scheduled.value,
            schedule="invalid cron",
        )

        # Should raise ValidationError
        with self.assertRaises(ValidationError):
            trigger.clean()

    def test_clean_non_scheduled_trigger_without_schedule(self):
        """Test that non-scheduled triggers don't require schedule"""
        trigger = WorkflowTrigger(
            slug="test-trigger",
            workflow=self.workflow,
            trigger_type=AutomationTriggerType.manual.value,
            schedule=None,
        )

        # Should not raise ValidationError
        trigger.clean()

    def test_update_next_run_at(self):
        """Test calculation of next run time based on cron schedule"""
        trigger = WorkflowTrigger.objects.create(
            slug="test-trigger",
            workflow=self.workflow,
            trigger_type=AutomationTriggerType.scheduled.value,
            schedule="0 9 * * 1",  # Every Monday at 9 AM
        )

        # Update next run time
        trigger.update_next_run()

        # Verify next_run_at was set
        self.assertIsNotNone(trigger.next_run_at)

        # Verify it's a future Monday at 9 AM
        self.assertEqual(trigger.next_run_at.hour, 9)
        self.assertEqual(trigger.next_run_at.minute, 0)
        self.assertEqual(trigger.next_run_at.weekday(), 0)  # Monday
        self.assertGreater(trigger.next_run_at, timezone.now())

    def test_is_due_property(self):
        """Test the is_due property for determining if workflow should run"""
        trigger = WorkflowTrigger.objects.create(
            slug="test-trigger",
            workflow=self.workflow,
            trigger_type=AutomationTriggerType.scheduled.value,
            schedule="0 9 * * 1",
        )

        # Set next_run_at to past time
        trigger.next_run_at = timezone.now() - datetime.timedelta(minutes=5)
        trigger.save()

        self.assertTrue(trigger.is_due)

        # Set next_run_at to future time
        trigger.next_run_at = timezone.now() + datetime.timedelta(minutes=5)
        trigger.save()

        self.assertFalse(trigger.is_due)


class TestScheduledWorkflowExecution(TestCase):
    """Test scheduled workflow execution"""

    def setUp(self):
        self.workflow = Workflow.objects.create(
            name="Test Workflow",
            slug="test-workflow",
            is_active=True,
        )

        self.trigger = WorkflowTrigger.objects.create(
            slug="test-trigger",
            workflow=self.workflow,
            trigger_type=AutomationTriggerType.scheduled.value,
            schedule="0 9 * * 1",
        )

    def test_scheduled_workflow_execution(self):
        """Test that scheduled workflows are executed correctly"""
        from karrio.server.automation.tasks import execute_scheduled_workflow

        # Execute the scheduled workflow
        execute_scheduled_workflow(self.trigger.id)

        # Verify workflow event was created
        events = WorkflowEvent.objects.filter(
            workflow=self.workflow,
            event_type=AutomationEventType.scheduled.value
        )
        self.assertEqual(events.count(), 1)

        # Verify trigger's last_run_at was updated
        self.trigger.refresh_from_db()
        self.assertIsNotNone(self.trigger.last_run_at)

        # Verify next_run_at was updated
        self.assertIsNotNone(self.trigger.next_run_at)
        self.assertGreater(self.trigger.next_run_at, self.trigger.last_run_at)

    def test_scheduled_workflow_execution_updates_trigger_times(self):
        """Test that execution updates trigger timing fields"""
        from karrio.server.automation.tasks import execute_scheduled_workflow

        # Record initial state
        initial_next_run = self.trigger.next_run_at

        # Execute scheduled workflow
        execute_scheduled_workflow(self.trigger.id)

        # Refresh trigger from database
        self.trigger.refresh_from_db()

        # Verify last_run_at was set
        self.assertIsNotNone(self.trigger.last_run_at)

        # Verify next_run_at was updated (if it was set initially)
        if initial_next_run:
            self.assertNotEqual(self.trigger.next_run_at, initial_next_run)


class TestScheduledWorkflowRegistry(TestCase):
    """Test the ScheduledWorkflowRegistry singleton"""

    def setUp(self):
        # Clear registry before each test
        ScheduledWorkflowRegistry.clear()

    def test_register_task(self):
        """Test registering a task in the registry"""
        trigger_id = "test-trigger-id"
        mock_task = Mock()

        ScheduledWorkflowRegistry.register(trigger_id, mock_task)

        self.assertIn(trigger_id, ScheduledWorkflowRegistry.get_registered_triggers())
        self.assertEqual(ScheduledWorkflowRegistry.get_task(trigger_id), mock_task)

    def test_unregister_task(self):
        """Test unregistering a task from the registry"""
        trigger_id = "test-trigger-id"
        mock_task = Mock()

        # Register first
        ScheduledWorkflowRegistry.register(trigger_id, mock_task)
        self.assertIn(trigger_id, ScheduledWorkflowRegistry.get_registered_triggers())

        # Unregister
        ScheduledWorkflowRegistry.unregister(trigger_id)
        self.assertNotIn(trigger_id, ScheduledWorkflowRegistry.get_registered_triggers())

    def test_clear_registry(self):
        """Test clearing all registered tasks"""
        # Register multiple tasks
        for i in range(3):
            ScheduledWorkflowRegistry.register(f"trigger-{i}", Mock())

        self.assertEqual(len(ScheduledWorkflowRegistry.get_registered_triggers()), 3)

        # Clear registry
        ScheduledWorkflowRegistry.clear()
        self.assertEqual(len(ScheduledWorkflowRegistry.get_registered_triggers()), 0)


class TestSignalHandlers(TestCase):
    """Test signal handlers for workflow trigger CRUD operations"""

    def setUp(self):
        self.workflow = Workflow.objects.create(
            name="Test Workflow",
            slug="test-workflow",
            is_active=True,
        )

    @patch('karrio.server.automation.services.scheduler.WorkflowScheduler.register_scheduled_workflow')
    def test_trigger_created_signal(self, mock_register):
        """Test that creating a scheduled trigger registers it"""
        trigger = WorkflowTrigger.objects.create(
            slug="test-trigger",
            workflow=self.workflow,
            trigger_type=AutomationTriggerType.scheduled.value,
            schedule="0 9 * * 1",
        )

        # Verify register_scheduled_workflow was called
        mock_register.assert_called_once_with(trigger)

    @patch('karrio.server.automation.services.scheduler.WorkflowScheduler.unregister_scheduled_workflow')
    def test_trigger_deleted_signal(self, mock_unregister):
        """Test that deleting a scheduled trigger unregisters it"""
        trigger = WorkflowTrigger.objects.create(
            slug="test-trigger",
            workflow=self.workflow,
            trigger_type=AutomationTriggerType.scheduled.value,
            schedule="0 9 * * 1",
        )

        # Delete the trigger
        trigger.delete()

        # Verify unregister_scheduled_workflow was called
        mock_unregister.assert_called_once_with(trigger)

    @patch('karrio.server.automation.services.scheduler.WorkflowScheduler.register_scheduled_workflow')
    @patch('karrio.server.automation.services.scheduler.WorkflowScheduler.unregister_scheduled_workflow')
    def test_trigger_updated_signal(self, mock_unregister, mock_register):
        """Test that updating a scheduled trigger re-registers it"""
        trigger = WorkflowTrigger.objects.create(
            slug="test-trigger",
            workflow=self.workflow,
            trigger_type=AutomationTriggerType.scheduled.value,
            schedule="0 9 * * 1",
        )

        # Clear previous calls from creation
        mock_register.reset_mock()
        mock_unregister.reset_mock()

        # Update the schedule
        trigger.schedule = "0 18 * * 1"  # Change to 6 PM
        trigger.save()

        # Verify re-registration happened
        mock_unregister.assert_called_once_with(trigger)
        mock_register.assert_called_once_with(trigger)


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class TestScheduledWorkflowIntegration(TestCase):
    """Integration tests for scheduled workflow functionality"""

    def setUp(self):
        self.workflow = Workflow.objects.create(
            name="Integration Test Workflow",
            slug="integration-test-workflow",
            is_active=True,
        )

    def test_end_to_end_scheduled_workflow(self):
        """Test complete flow from trigger creation to execution"""
        # Create scheduled trigger
        trigger = WorkflowTrigger.objects.create(
            slug="integration-test-trigger",
            workflow=self.workflow,
            trigger_type=AutomationTriggerType.scheduled.value,
            schedule="* * * * *",  # Every minute for testing
        )

        # Verify trigger was registered
        self.assertIn(trigger.id, ScheduledWorkflowRegistry.get_registered_triggers())

        # Simulate task execution
        from karrio.server.automation.tasks import execute_scheduled_workflow
        execute_scheduled_workflow(trigger.id)

        # Verify workflow event was created
        events = WorkflowEvent.objects.filter(
            workflow=self.workflow,
            event_type=AutomationEventType.scheduled.value
        )
        self.assertEqual(events.count(), 1)

        # Verify trigger times were updated
        trigger.refresh_from_db()
        self.assertIsNotNone(trigger.last_run_at)
        self.assertIsNotNone(trigger.next_run_at)

    def test_high_frequency_scheduled_workflow(self):
        """Test scheduled workflow that runs very frequently (every second simulation)"""
        # Create a workflow that would run every minute (closest to every second in cron)
        trigger = WorkflowTrigger.objects.create(
            slug="high-frequency-trigger",
            workflow=self.workflow,
            trigger_type=AutomationTriggerType.scheduled.value,
            schedule="* * * * *",  # Every minute - highest frequency for standard cron
        )

        # Set next_run_at to past time to simulate it being due
        past_time = timezone.now() - datetime.timedelta(seconds=5)
        trigger.next_run_at = past_time
        trigger.save()

        # Verify trigger is due
        self.assertTrue(trigger.is_due)

        # Execute the workflow multiple times to simulate rapid execution
        from karrio.server.automation.tasks import execute_scheduled_workflow

        # First execution
        execute_scheduled_workflow(trigger.id)
        trigger.refresh_from_db()
        first_execution_time = trigger.last_run_at
        first_next_run = trigger.next_run_at

        # Verify first execution worked
        self.assertIsNotNone(first_execution_time)
        self.assertIsNotNone(first_next_run)
        self.assertGreater(first_next_run, first_execution_time)

        # Simulate second execution shortly after (set next_run to past again)
        trigger.next_run_at = timezone.now() - datetime.timedelta(seconds=1)
        trigger.save()

        # Second execution
        execute_scheduled_workflow(trigger.id)
        trigger.refresh_from_db()
        second_execution_time = trigger.last_run_at
        second_next_run = trigger.next_run_at

        # Verify second execution updated times
        self.assertGreater(second_execution_time, first_execution_time)
        self.assertGreater(second_next_run, second_execution_time)

        # Verify we have 2 workflow events
        events = WorkflowEvent.objects.filter(
            workflow=self.workflow,
            event_type=AutomationEventType.scheduled.value
        ).order_by('created_at')
        self.assertEqual(events.count(), 2)

        # Verify event parameters contain correct scheduling info
        event = events.first()
        self.assertIn('trigger_id', event.parameters)
        self.assertIn('execution_time', event.parameters)
        self.assertIn('scheduled', event.parameters)
        self.assertTrue(event.parameters['scheduled'])
        self.assertEqual(event.parameters['trigger_id'], trigger.id)

    def test_concurrent_scheduled_workflows(self):
        """Test multiple scheduled workflows running concurrently"""
        workflows = []
        triggers = []

        # Create 3 different workflows with different schedules
        schedules = [
            ("* * * * *", "every-minute"),      # Every minute
            ("0 * * * *", "every-hour"),       # Every hour
            ("0 0 * * *", "every-day"),        # Every day
        ]

        for i, (schedule, slug_suffix) in enumerate(schedules):
            workflow = Workflow.objects.create(
                name=f"Concurrent Test Workflow {i}",
                slug=f"concurrent-test-workflow-{i}",
                is_active=True,
            )
            workflows.append(workflow)

            trigger = WorkflowTrigger.objects.create(
                slug=f"concurrent-trigger-{slug_suffix}",
                workflow=workflow,
                trigger_type=AutomationTriggerType.scheduled.value,
                schedule=schedule,
            )
            triggers.append(trigger)

            # Set all triggers to be due now
            trigger.next_run_at = timezone.now() - datetime.timedelta(seconds=1)
            trigger.save()

        # Execute all workflows
        from karrio.server.automation.tasks import execute_scheduled_workflow
        for trigger in triggers:
            execute_scheduled_workflow(trigger.id)

        # Verify all workflows executed
        for i, workflow in enumerate(workflows):
            events = WorkflowEvent.objects.filter(
                workflow=workflow,
                event_type=AutomationEventType.scheduled.value
            )
            self.assertEqual(events.count(), 1, f"Workflow {i} should have 1 event")

        # Verify all triggers were updated
        for trigger in triggers:
            trigger.refresh_from_db()
            self.assertIsNotNone(trigger.last_run_at)
            self.assertIsNotNone(trigger.next_run_at)

    def test_scheduled_workflow_error_handling(self):
        """Test error handling in scheduled workflow execution"""
        # Create trigger with invalid workflow reference
        trigger = WorkflowTrigger.objects.create(
            slug="error-test-trigger",
            workflow=self.workflow,
            trigger_type=AutomationTriggerType.scheduled.value,
            schedule="* * * * *",
        )

        # Delete the workflow to create invalid reference
        workflow_id = self.workflow.id
        self.workflow.delete()

        # Execute should handle the error gracefully
        from karrio.server.automation.tasks import execute_scheduled_workflow

        # This should not raise an exception
        execute_scheduled_workflow(trigger.id)

        # Verify no workflow event was created for the deleted workflow
        events = WorkflowEvent.objects.filter(
            event_type=AutomationEventType.scheduled.value
        )
        self.assertEqual(events.count(), 0)

    def test_inactive_workflow_skipped(self):
        """Test that inactive workflows are skipped during execution"""
        trigger = WorkflowTrigger.objects.create(
            slug="inactive-test-trigger",
            workflow=self.workflow,
            trigger_type=AutomationTriggerType.scheduled.value,
            schedule="* * * * *",
        )

        # Make workflow inactive after trigger creation
        self.workflow.is_active = False
        self.workflow.save()

        # Execute scheduled workflow
        from karrio.server.automation.tasks import execute_scheduled_workflow

        # Should execute without raising an exception
        execute_scheduled_workflow(trigger.id)

        # Verify no workflow event was created
        events = WorkflowEvent.objects.filter(
            workflow=self.workflow,
            event_type=AutomationEventType.scheduled.value
        )
        self.assertEqual(events.count(), 0)

        # Verify trigger timestamps were not updated
        trigger.refresh_from_db()
        self.assertIsNone(trigger.last_run_at)


class TestCronValidation(TestCase):
    """Test cron expression validation utilities"""

    def test_valid_cron_expressions(self):
        """Test validation of valid cron expressions"""
        from karrio.server.automation.cron_utils import validate_cron_expression

        valid_expressions = [
            "0 9 * * 1",        # Every Monday at 9 AM
            "*/15 * * * *",     # Every 15 minutes
            "0 0 1 * *",        # First day of every month
            "0 12 * * 1-5",     # Weekdays at noon
            "30 2 * * 0",       # Sundays at 2:30 AM
        ]

        for expr in valid_expressions:
            with self.subTest(expr=expr):
                # Should not raise exception
                validate_cron_expression(expr)

    def test_invalid_cron_expressions(self):
        """Test validation of invalid cron expressions"""
        from karrio.server.automation.cron_utils import validate_cron_expression
        from karrio.server.automation.exceptions import InvalidCronExpressionError

        invalid_expressions = [
            "invalid",          # Not a cron expression
            "0 25 * * *",       # Invalid hour (25)
            "60 0 * * *",       # Invalid minute (60)
            "0 0 32 * *",       # Invalid day (32)
            "0 0 * 13 *",       # Invalid month (13)
            "0 0 * * 8",        # Invalid weekday (8)
        ]

        for expr in invalid_expressions:
            with self.subTest(expr=expr):
                with self.assertRaises(InvalidCronExpressionError):
                    validate_cron_expression(expr)

    def test_calculate_next_run_time(self):
        """Test calculation of next run time from cron expression"""
        from karrio.server.automation.cron_utils import calculate_next_run_time

        # Test "every Monday at 9 AM"
        base_time = timezone.make_aware(datetime.datetime(2024, 1, 15, 10, 0))  # Monday at 10 AM
        next_run = calculate_next_run_time("0 9 * * 1", base_time)

        # Should be next Monday at 9 AM
        self.assertEqual(next_run.hour, 9)
        self.assertEqual(next_run.minute, 0)
        self.assertEqual(next_run.weekday(), 0)  # Monday
        self.assertGreater(next_run, base_time)
