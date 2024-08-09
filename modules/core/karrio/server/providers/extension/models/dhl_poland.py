import django.db.models as models
import karrio.server.providers.models as providers


# @providers.has_rate_sheet("dhl_poland")
class DHLPolandSettings(providers.Carrier):
    class Meta:
        db_table = "dhl-poland-settings"
        verbose_name = "DHL Poland Settings"
        verbose_name_plural = "DHL Poland Settings"

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200, blank=True)
    services = models.ManyToManyField("ServiceLevel", blank=True)

    @property
    def carrier_name(self) -> str:
        return "dhl_poland"


SETTINGS = DHLPolandSettings
