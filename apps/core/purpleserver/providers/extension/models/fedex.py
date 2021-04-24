from django.db import models
from purpleserver.providers.models.carrier import Carrier


class FedexSettings(Carrier):
    CARRIER_NAME = 'fedex'

    class Meta:
        db_table = "fedex-settings"
        verbose_name = 'FedEx Settings'
        verbose_name_plural = 'FedEx Settings'

    user_key = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    meter_number = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = FedexSettings
