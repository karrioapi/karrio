from django.db import models
import karrio.server.providers.models.carrier as providers


class Zoom2uSettings(providers.Carrier):
    CARRIER_NAME = "zoom2u"

    class Meta:
        db_table = "zoom2u-settings"
        verbose_name = "Zoom2u Settings"
        verbose_name_plural = "Zoom2u Settings"

    api_key = models.CharField(max_length=200)
    account_country_code = models.CharField(
        max_length=3, blank=True, null=True, choices=providers.COUNTRIES
    )

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = Zoom2uSettings
