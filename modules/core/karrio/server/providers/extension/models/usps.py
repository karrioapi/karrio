import django.db.models as models
import karrio.server.providers.models as providers


class USPSSettings(providers.Carrier):
    CARRIER_NAME = "usps"

    class Meta:
        db_table = "usps-settings"
        verbose_name = "USPS Settings"
        verbose_name_plural = "USPS Settings"

    client_id = models.CharField(max_length=100)
    client_secret = models.CharField(max_length=100)
    account_type = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(max_length=100, blank=True, null=True)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = USPSSettings
