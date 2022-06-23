from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuditConfig(AppConfig):
    name = "karrio.server.audit"
    verbose_name = _("Audit Log")
    default_auto_field = "django.db.models.BigAutoField"
