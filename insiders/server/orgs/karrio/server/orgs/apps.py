from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrgsConfig(AppConfig):
    name = "karrio.server.orgs"
    verbose_name = _("Organizations")

    def ready(self):
        from karrio.server.orgs import signals

        signals.register_all()
