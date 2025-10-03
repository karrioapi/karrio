"""
Workflow Test Base Classes

This module provides base test classes for workflow automation testing.

Usage:
    Run tests with immediate Huey execution:
    $ WORKER_IMMEDIATE_MODE=True karrio test karrio.server.automation.tests

The WORKER_IMMEDIATE_MODE environment variable enables synchronous task execution
for reliable testing without requiring a background Huey consumer.
"""

import karrio.server.graph.tests.base as base
import karrio.server.automation.models as models
from django.test import override_settings
import time

# Enhanced SQLite settings for workflow testing with concurrency handling
TEST_DATABASE_SETTINGS = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'OPTIONS': {
            'timeout': 60,
            'isolation_level': None,  # Autocommit mode for concurrency
        },
        'TEST': {
            'NAME': ':memory:',
        }
    }
}

@override_settings(DATABASES=TEST_DATABASE_SETTINGS)
class WorkflowTestCase(base.GraphTestCase):
    """
    Base test case for workflow automation tests.

    Provides common workflow setup and utilities for testing workflow execution,
    action processing, and event handling.

    Note:
        Tests must be run with WORKER_IMMEDIATE_MODE=True environment variable
        to enable synchronous task execution.
    """

    def setUp(self):
        self.maxDiff = None
        super().setUp()
        self._create_test_fixtures()

    def _create_test_fixtures(self):
        """Create standard test workflow and action for testing."""
        self.action = models.WorkflowAction.objects.create(
            name="Karrio metadata",
            action_type="http_request",
            host="https://api.karrio.io",
            method="get",
            slug="$.test.workflow.action",
            header_template='{ "Content-type": "application/json" }',
            created_by=self.user,
        )

        self.workflow = models.Workflow.objects.create(
            name="Karrio connection validation",
            slug="$.test.workflow",
            action_nodes=[{"slug": "$.test.workflow.action", "order": 0}],
            created_by=self.user,
        )

    def wait_for_workflow_completion(self, event_id: str, timeout: int = 5):
        """
        Wait for workflow execution to complete.

        With WORKER_IMMEDIATE_MODE=True, tasks execute synchronously but may
        require brief waiting for database commits and status updates.

        Args:
            event_id: The workflow event ID to monitor
            timeout: Maximum seconds to wait for completion

        Returns:
            WorkflowEvent: The completed workflow event

        Raises:
            TimeoutError: If workflow doesn't complete within timeout
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                event = models.WorkflowEvent.objects.get(id=event_id)
                if event.status in ['success', 'failed', 'cancelled']:
                    return event
            except Exception:
                pass
            time.sleep(0.1)

        # Final status check
        try:
            event = models.WorkflowEvent.objects.get(id=event_id)
            return event
        except Exception as e:
            raise TimeoutError(f"Workflow event {event_id} not found: {str(e)}")
