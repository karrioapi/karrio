from django.db import models
from karrio.server.providers.models.carrier import Carrier, COUNTRIES


class FedexWSSettings(Carrier):
    class Meta:
        db_table = "fedex-ws-settings"
        verbose_name = "FedEx Web Service Settings"
        verbose_name_plural = "FedEx Web Service Settings"

    password = models.CharField(max_length=200)
    meter_number = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
    user_key = models.CharField(max_length=200, blank=True)
    account_country_code = models.CharField(
        max_length=3, blank=True, null=True, choices=COUNTRIES
    )

    @property
    def carrier_name(self) -> str:
        return "fedex"


SETTINGS = FedexWSSettings
