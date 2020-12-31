from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'purpleserver.core'
    # verbose_name = "Carriers"

    def ready(self):
        import purpleserver.core.signals
