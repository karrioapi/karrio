from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EventsConfig(AppConfig):
    name = 'karrio.server.events'
    verbose_name = _('Custom Pricing')

    def ready(self):
        from karrio.server.events import signals
        signals.register_signals()
