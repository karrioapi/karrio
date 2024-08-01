import django.db.models as models
import karrio.server.providers.models as providers


@providers.has_rate_sheet("sapient")
class SAPIENTSettings(providers.Carrier):
    class Meta:
        db_table = "sapient-settings"
        verbose_name = "SAPIENT Settings"
        verbose_name_plural = "SAPIENT Settings"

    client_id = models.CharField(max_length=100)
    client_secret = models.CharField(max_length=100)
    shipping_account_id = models.CharField(max_length=100)
    services = models.ManyToManyField("ServiceLevel", blank=True)

    @property
    def carrier_name(self) -> str:
        return "sapient"


SETTINGS = SAPIENTSettings
