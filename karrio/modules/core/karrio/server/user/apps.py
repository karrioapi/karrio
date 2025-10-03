from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserConfig(AppConfig):
    name = "karrio.server.user"
    verbose_name = _("AUTHENTICATION AND AUTHORIZATION")
