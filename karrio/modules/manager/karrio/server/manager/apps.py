from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ManagerConfig(AppConfig):
    name = "karrio.server.manager"
    verbose_name = _("Shipment Manager")
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from karrio.server.manager import signals

        signals.register_signals()
