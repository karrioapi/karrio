import django.db.models as models
import karrio.server.providers.models as providers


class SendleSettings(providers.Carrier):
    class Meta:
        db_table = "sendle-settings"
        verbose_name = "Sendle Settings"
        verbose_name_plural = "Sendle Settings"

    sendle_id = models.CharField(max_length=200)
    api_key = models.CharField(max_length=200)
    account_country_code = models.CharField(
        max_length=3, blank=True, null=True, choices=providers.COUNTRIES
    )

    @property
    def carrier_name(self) -> str:
        return "sendle"


SETTINGS = SendleSettings
