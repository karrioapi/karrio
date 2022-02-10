from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrdersConfig(AppConfig):
    name = "purplship.server.orders"
    verbose_name = _("Orders")
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from purplship.server.orders import signals

        signals.register_signals()
