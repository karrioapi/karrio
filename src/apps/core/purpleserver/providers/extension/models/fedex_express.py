from django.db import models
from purpleserver.providers.models.carrier import Carrier


class FedexExpressSettings(Carrier):
    CARRIER_NAME = 'fedex_express'

    class Meta:
        db_table = "fedex_express-settings"
        verbose_name = 'FedEx Express Settings'
        verbose_name_plural = 'FedEx Express Settings'

    user_key = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    meter_number = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = FedexExpressSettings
