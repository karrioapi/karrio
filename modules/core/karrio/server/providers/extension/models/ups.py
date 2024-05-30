import django.db.models as models
import karrio.server.providers.models as providers


class UPSSettings(providers.Carrier):
    class Meta:
        db_table = "ups-settings"
        verbose_name = "UPS Settings"
        verbose_name_plural = "UPS Settings"

    client_id = models.CharField(max_length=200)
    client_secret = models.CharField(max_length=200)
    account_number = models.CharField(blank=True, null=True, max_length=100)
    account_country_code = models.CharField(
        max_length=3, blank=True, null=True, choices=providers.COUNTRIES
    )

    @property
    def carrier_name(self) -> str:
        return "ups"


SETTINGS = UPSSettings
