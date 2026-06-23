from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "karrio.server.core"

    def ready(self):
        from karrio.server.core.signals import register_signals
        from karrio.server.core import checks  # noqa: F401 — registers system checks

        register_signals()
        # Telemetry PII scrubbing (karrio.server.core.telemetry_scrubbing) is now
        # a dependency-free, deterministic regex/structural scrubber — no engine
        # to pre-warm (issue #641).
