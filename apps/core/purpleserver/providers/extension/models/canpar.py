from django.db import models
from purpleserver.providers.models.carrier import Carrier


class CanparSettings(Carrier):
    CARRIER_NAME = 'canpar'

    class Meta:
        db_table = "canpar-settings"
        verbose_name = 'Canpar Settings'
        verbose_name_plural = 'Canpar Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = CanparSettings
