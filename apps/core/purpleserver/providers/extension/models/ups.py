from django.db import models
from purpleserver.providers.models.carrier import Carrier


class UPSSettings(Carrier):
    CARRIER_NAME = 'ups'

    class Meta:
        db_table = "ups-settings"
        verbose_name = 'UPS Settings'
        verbose_name_plural = 'UPS Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    access_license_number = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = UPSSettings
