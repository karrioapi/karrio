from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "karrio.server.core"

    def ready(self):
        from karrio.server.core import checks  # noqa: F401 — registers system checks
        from karrio.server.core.signals import register_signals

        register_signals()
