from django.apps import AppConfig


class ManagerConfig(AppConfig):
    name = "karrio.server.manager"

    def ready(self):
        from karrio.server.manager import signals

        signals.register_signals()
