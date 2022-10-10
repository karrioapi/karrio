from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrdersConfig(AppConfig):
    name = "karrio.server.orders"
    verbose_name = _("Orders")
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from karrio.server.orders import signals

        signals.register_signals()
