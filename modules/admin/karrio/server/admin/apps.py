from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdminConfig(AppConfig):
    label = "karrio_admin"
    name = "karrio.server.admin"
    verbose_name = _("Karrio Admin")
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from karrio.server.admin import signals

        signals.register_signals()
