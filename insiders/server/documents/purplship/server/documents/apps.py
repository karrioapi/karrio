from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DocumentsConfig(AppConfig):
    name = "purplship.server.documents"
    verbose_name = _("Documents")
    default_auto_field = "django.db.models.BigAutoField"
