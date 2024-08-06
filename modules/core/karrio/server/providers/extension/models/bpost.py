import django.db.models as models
import karrio.server.providers.models as providers


# @providers.has_rate_sheet("bpost")
class BelgianPostSettings(providers.Carrier):
    class Meta:
        db_table = "bpost-settings"
        verbose_name = "Belgian Post Settings"
        verbose_name_plural = "Belgian Post Settings"

    account_id = models.CharField(max_length=100)
    passphrase = models.CharField(max_length=100)
    services = models.ManyToManyField("ServiceLevel", blank=True)

    @property
    def carrier_name(self) -> str:
        return "bpost"


SETTINGS = BelgianPostSettings
