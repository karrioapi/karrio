import django.db.models as models
import karrio.server.providers.models.carrier as providers


class AsendiaUSSettings(providers.Carrier):
    class Meta:
        db_table = "asendia-us-settings"
        verbose_name = "Asendia US Settings"
        verbose_name_plural = "Asendia US Settings"

    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100, blank=True)

    @property
    def carrier_name(self) -> str:
        return "asendia_us"


SETTINGS = AsendiaUSSettings
