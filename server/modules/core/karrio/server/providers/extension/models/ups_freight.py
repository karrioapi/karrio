from django.db import models
from karrio.server.providers.models.carrier import Carrier, COUNTRIES


class UPSFreightSettings(Carrier):
    class Meta:
        db_table = "ups_freight-settings"
        verbose_name = 'UPS Freight Settings'
        verbose_name_plural = 'UPS Freight Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    access_license_number = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
    account_country_code = models.CharField(max_length=3, blank=True, choices=COUNTRIES)

    @property
    def carrier_name(self) -> str:
        return 'ups_freight'


SETTINGS = UPSFreightSettings
