from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EventsConfig(AppConfig):
    name = 'purpleserver.events'
    verbose_name = _('Custom Pricing')

    def ready(self):
        from purpleserver.events import signals
        signals.register_signals()
