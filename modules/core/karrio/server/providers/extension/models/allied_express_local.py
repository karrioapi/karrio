import django.db.models as models

import karrio.server.providers.models.carrier as providers


class AlliedExpressLocalSettings(providers.Carrier):
    class Meta:
        db_table = "allied-express-local-settings"
        verbose_name = "Allied Express Local Settings"
        verbose_name_plural = "Allied Express Local Settings"

    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    account = models.CharField(max_length=50, null=True, blank=True)
    service_type = models.CharField(max_length=50, null=True, blank=True)

    @property
    def carrier_name(self) -> str:
        return "allied_express_local"


SETTINGS = AlliedExpressLocalSettings
