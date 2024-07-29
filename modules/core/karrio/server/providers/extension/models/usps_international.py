from django.db import models
from karrio.server.providers.models.carrier import Carrier


class USPSInternationalSettings(Carrier):
    CARRIER_NAME = "usps_international"

    class Meta:
        db_table = "usps_international-settings"
        verbose_name = "USPS International Settings"
        verbose_name_plural = "USPS International Settings"

    client_id = models.CharField(max_length=100)
    client_secret = models.CharField(max_length=100)
    account_type = models.CharField(max_length=200, null=True, blank=True)
    account_number = models.CharField(max_length=200, blank=True, null=True)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = USPSInternationalSettings
