from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShippingConfig(AppConfig):
    name = "karrio.server.shipping"
    verbose_name = _("JTL Shipping")

    def ready(self):
        from karrio.server.shipping import signals

        signals.register_all()
