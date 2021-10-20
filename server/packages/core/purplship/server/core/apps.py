from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'purplship.server.core'

    def ready(self):
        from constance import config
        from constance.signals import config_updated
        from purplship.server.core.signals import update_settings, constance_updated
        config_updated.connect(constance_updated)
        update_settings(config)
