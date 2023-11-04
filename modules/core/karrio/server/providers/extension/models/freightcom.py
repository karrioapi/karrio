from django.db import models
from karrio.server.providers.models.carrier import Carrier


class FreightcomSettings(Carrier):
    CARRIER_NAME = 'freightcom'

    class Meta:
        db_table = "freightcom-settings"
        verbose_name = 'Freightcom Settings'
        verbose_name_plural = 'Freightcom Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = FreightcomSettings
