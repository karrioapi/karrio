import django.db.models as models
import karrio.server.providers.models as providers


class FedexSettings(providers.Carrier):
    class Meta:
        db_table = "fedex-settings"
        verbose_name = "FedEx Settings"
        verbose_name_plural = "FedEx Settings"

    api_key = models.CharField(max_length=100, blank=True, null=True)
    secret_key = models.CharField(max_length=100, blank=True, null=True)
    track_api_key = models.CharField(max_length=100, blank=True, null=True)
    track_secret_key = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    account_country_code = models.CharField(
        max_length=3, blank=True, null=True, choices=providers.COUNTRIES
    )

    @property
    def carrier_name(self) -> str:
        return "fedex"


SETTINGS = FedexSettings
