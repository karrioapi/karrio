from django.db import models
from purpleserver.providers.models.carrier import Carrier


class DHLUniversalSettings(Carrier):
    CARRIER_NAME = 'dhl_universal'

    class Meta:
        db_table = "dhl_universal-settings"
        verbose_name = 'DHL Universal Tracking Settings'
        verbose_name_plural = 'DHL Universal Tracking Settings'

    consumer_key = models.CharField(max_length=200)
    consumer_secret = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = DHLUniversalSettings
