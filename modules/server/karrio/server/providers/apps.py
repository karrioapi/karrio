from django.apps import AppConfig


class ProvidersConfig(AppConfig):
    name = "karrio.server.providers"

    def ready(self):
        from karrio.server.providers import signals

        signals.register_signals()
