from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DataConfig(AppConfig):
    name = "karrio.server.data"
    verbose_name = _("Import/Export")
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from karrio.server.data import signals

        signals.register_all()
