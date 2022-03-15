from django.db import models
from karrio.server.providers.models.carrier import Carrier


class CanparSettings(Carrier):
    class Meta:
        db_table = "canpar-settings"
        verbose_name = 'Canpar Settings'
        verbose_name_plural = 'Canpar Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return 'canpar'


SETTINGS = CanparSettings
