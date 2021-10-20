from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EventsConfig(AppConfig):
    name = 'purplship.server.events'
    verbose_name = _('Custom Pricing')

    def ready(self):
        from purplship.server.events import signals
        signals.register_signals()
