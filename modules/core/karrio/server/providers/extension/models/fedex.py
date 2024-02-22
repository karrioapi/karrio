import django.db.models as models
import karrio.server.providers.models as providers


@providers.has_auth_cache
class FedexSettings(providers.Carrier):
    class Meta:
        db_table = "fedex-settings"
        verbose_name = "FedEx Settings"
        verbose_name_plural = "FedEx Settings"

    api_key = models.CharField(max_length=200)
    secret_key = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
    account_country_code = models.CharField(
        max_length=3, blank=True, null=True, choices=providers.COUNTRIES
    )

    @property
    def carrier_name(self) -> str:
        return "fedex"


SETTINGS = FedexSettings
