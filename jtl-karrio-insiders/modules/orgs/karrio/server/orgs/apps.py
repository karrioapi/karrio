from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrgsConfig(AppConfig):
    name = "karrio.server.orgs"
    verbose_name = _("Organizations")

    def ready(self):
        from karrio.server.core import utils
        from karrio.server.orgs import signals, permissions

        @utils.skip_on_commands()
        def _init():
            signals.register_all()

            # Setup default permission groups and apply to existing orgs on start up
            utils.run_on_all_tenants(permissions.apply_for_org_users)()

        _init()

        signals.register_all()
