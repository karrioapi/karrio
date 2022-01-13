from django.apps import AppConfig


class ManagerConfig(AppConfig):
    name = "purplship.server.manager"

    def ready(self):
        from purplship.server.manager import signals

        signals.register_signals()
