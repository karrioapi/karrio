from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrgsConfig(AppConfig):
    name = "purplship.server.orgs"
    verbose_name = _("Organizations")

    def ready(self):
        from purplship.server.orgs import signals

        signals.register_all()
