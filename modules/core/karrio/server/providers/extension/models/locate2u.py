import django.db.models as models
import karrio.server.providers.models.carrier as providers


class Locate2uSettings(providers.Carrier):
    class Meta:
        db_table = "locate2u-settings"
        verbose_name = "Locate2u Settings"
        verbose_name_plural = "Locate2u Settings"

    client_id = models.CharField(max_length=200)
    client_secret = models.CharField(max_length=200)
    account_country_code = models.CharField(
        max_length=3, blank=True, null=True, choices=providers.COUNTRIES
    )

    @property
    def carrier_name(self) -> str:
        return "locate2u"


SETTINGS = Locate2uSettings
