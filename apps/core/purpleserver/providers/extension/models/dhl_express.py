from django.db import models
from purpleserver.providers.models.carrier import Carrier


class DHLExpressSettings(Carrier):
    CARRIER_NAME = 'dhl_express'

    class Meta:
        db_table = "dhl_express-settings"
        verbose_name = 'DHL Express Settings'
        verbose_name_plural = 'DHL Express Settings'

    site_id = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200, blank=True, default='')

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = DHLExpressSettings
