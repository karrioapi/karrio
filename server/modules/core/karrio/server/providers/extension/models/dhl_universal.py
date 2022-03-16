from django.db import models
from karrio.server.providers.models.carrier import Carrier


class DHLUniversalSettings(Carrier):
    class Meta:
        db_table = "dhl_universal-settings"
        verbose_name = 'DHL Universal Tracking Settings'
        verbose_name_plural = 'DHL Universal Tracking Settings'

    consumer_key = models.CharField(max_length=200)
    consumer_secret = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return 'dhl_universal'


SETTINGS = DHLUniversalSettings
