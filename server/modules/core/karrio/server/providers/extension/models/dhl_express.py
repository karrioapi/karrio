from django.db import models
from karrio.server.providers.models.carrier import Carrier, COUNTRIES


class DHLExpressSettings(Carrier):
    class Meta:
        db_table = "dhl_express-settings"
        verbose_name = 'DHL Express Settings'
        verbose_name_plural = 'DHL Express Settings'

    site_id = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200, blank=True, default='')
    account_country_code = models.CharField(max_length=3, blank=True, choices=COUNTRIES)

    @property
    def carrier_name(self) -> str:
        return 'dhl_express'


SETTINGS = DHLExpressSettings
