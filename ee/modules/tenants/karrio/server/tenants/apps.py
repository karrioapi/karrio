from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TenantsConfig(AppConfig):
    name = "karrio.server.tenants"
    verbose_name = _("Tenant Management")

    def ready(self):
        from karrio.server.tenants import signals

        signals.register_all()
