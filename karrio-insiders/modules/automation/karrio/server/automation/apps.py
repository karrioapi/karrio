import os
import logging
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class AutomationConfig(AppConfig):
    name = "karrio.server.automation"
    verbose_name = _("Automation")
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        import karrio.server.automation.signals as signals

        signals.register()

        # # Load scheduled workflows only in worker processes
        # if self._should_register_scheduled_workflows():
        #     self._register_scheduled_workflows()

    def _should_register_scheduled_workflows(self) -> bool:
        """
        Determine if this process should register scheduled workflows.

        We only want to register scheduled workflows in worker processes,
        not in web server processes or management commands.
        """
        # Check if we're running the Huey consumer
        import sys

        command_args = " ".join(sys.argv)

        # Register in Huey consumer processes
        if "run_huey" in command_args:
            return True

        # Register in development runserver if no separate worker
        if (
            "runserver" in command_args
            and os.environ.get("DJANGO_DEVELOPMENT_MODE", "False").lower() == "true"
        ):
            return True

        # Don't register in migrations, tests, or other management commands
        if any(
            cmd in command_args
            for cmd in ["migrate", "test", "makemigrations", "shell"]
        ):
            return False

        return False

    def _register_scheduled_workflows(self):
        """Register all scheduled workflows from the database."""
        try:
            from karrio.server.automation.services.scheduler import workflow_scheduler

            # Small delay to ensure database is ready
            import time

            time.sleep(1)

            registered_count = workflow_scheduler.refresh_all_scheduled_workflows()
            logger.info(
                f"Automation app ready: {registered_count} scheduled workflows registered"
            )

        except Exception as e:
            logger.error(f"Failed to register scheduled workflows on startup: {e}")
            # Don't raise exception to avoid breaking app startup
