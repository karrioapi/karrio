import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class HueyConfig(AppConfig):
    name = "karrio.server.huey"
    verbose_name = "Karrio Huey Worker"

    def ready(self):
        from django.conf import settings
        from karrio.server.core.task_backend import set_backend

        task_backend = getattr(settings, "TASK_BACKEND", "huey")
        worker_immediate = getattr(settings, "WORKER_IMMEDIATE_MODE", False)

        # Import backend eagerly so the generic dispatcher is registered in
        # Huey's TaskRegistry for both API and worker processes.
        from karrio.server.huey.backend import HueyBackend  # noqa: F401

        if task_backend == "huey" and not worker_immediate:
            set_backend(HueyBackend())
            logger.info("Registered HueyBackend as active task backend")

        self._register_signals()
        self._instrument_otel()

    def _register_signals(self):
        try:
            from karrio.server.huey.signals import register_huey_signals

            register_huey_signals()
        except Exception as e:
            logger.debug("Huey signal registration skipped: %s", e)

    def _instrument_otel(self):
        from django.conf import settings

        if not getattr(settings, "OTEL_ENABLED", False):
            return

        try:
            from karrio.server.huey.instrumentation import HueyInstrumentor

            HueyInstrumentor().instrument()
        except Exception as e:
            logger.debug("Huey OTel instrumentation skipped: %s", e)
