from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TracingConfig(AppConfig):
    name = "karrio.server.tracing"
    verbose_name = _("Tracing")
    default_auto_field = "django.db.models.BigAutoField"
