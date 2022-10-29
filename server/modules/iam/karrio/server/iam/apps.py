from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class IamConfig(AppConfig):
    name = "karrio.server.iam"
    verbose_name = _("IAM")
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from karrio.server.core import utils
        from karrio.server.iam import signals, permissions

        @utils.skip_on_commands()
        def _init():
            signals.register_all()

            # Setup default permission groups and apply to existing orgs on start up
            utils.run_on_all_tenants(permissions.setup_groups)()

        _init()
