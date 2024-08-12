import django.db.models as models
import karrio.server.providers.models as providers


# @providers.has_rate_sheet("dpdhl")
class DPDHLSettings(providers.Carrier):
    class Meta:
        db_table = "dpdhl-settings"
        verbose_name = "Deutsche Post DHL Settings"
        verbose_name_plural = "Deutsche Post DHL Settings"

    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    zt_id = models.CharField(max_length=100, blank=True, null=True, default="")
    zt_password = models.CharField(max_length=100, blank=True, null=True, default="")
    app_id = models.CharField(max_length=100, blank=True, null=True, default="")
    app_token = models.CharField(max_length=100, blank=True, null=True, default="")
    account_number = models.CharField(max_length=100, blank=True, null=True, default="")
    services = models.ManyToManyField("ServiceLevel", blank=True)

    @property
    def carrier_name(self) -> str:
        return "dpdhl"


SETTINGS = DPDHLSettings
