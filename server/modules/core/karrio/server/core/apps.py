from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'karrio.server.core'

    def ready(self):
        from constance import config
        from constance.signals import config_updated
        from karrio.server.core.signals import update_settings, constance_updated
        config_updated.connect(constance_updated)
        update_settings(config)
