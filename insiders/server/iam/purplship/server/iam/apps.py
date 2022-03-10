from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class IamConfig(AppConfig):
    name = "purplship.server.iam"
    verbose_name = _("IAM")
    default_auto_field = "django.db.models.BigAutoField"
