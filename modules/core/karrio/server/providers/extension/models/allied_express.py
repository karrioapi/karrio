import django.db.models as models

import karrio.server.providers.models.carrier as providers


class AlliedExpressSettings(providers.Carrier):
    class Meta:
        db_table = "allied-express-settings"
        verbose_name = "Allied Express Settings"
        verbose_name_plural = "Allied Express Settings"

    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    account = models.CharField(max_length=50, null=True, blank=True)
    service_type = models.CharField(max_length=50, null=True, blank=True)

    @property
    def carrier_name(self) -> str:
        return "allied_express"


SETTINGS = AlliedExpressSettings
