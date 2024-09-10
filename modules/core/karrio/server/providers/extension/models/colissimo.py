import django.db.models as models
import karrio.server.providers.models as providers


# @providers.has_rate_sheet("colissimo")
class ColissimoSettings(providers.Carrier):
    class Meta:
        db_table = "colissimo-settings"
        verbose_name = "Colissimo Settings"
        verbose_name_plural = "Colissimo Settings"

    password = models.CharField(max_length=100)
    contract_number = models.CharField(max_length=100)
    laposte_api_key = models.CharField(max_length=100, blank=True)
    services = models.ManyToManyField("ServiceLevel", blank=True)

    @property
    def carrier_name(self) -> str:
        return "colissimo"


SETTINGS = ColissimoSettings
