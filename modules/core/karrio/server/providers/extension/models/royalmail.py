from django.db import models
from karrio.server.providers.models.carrier import Carrier


class RoyalMailSettings(Carrier):
    class Meta:
        db_table = "royalmail-settings"
        verbose_name = 'Royal Mail Settings'
        verbose_name_plural = 'Royal Mail Settings'

    client_id = models.CharField(max_length=200)
    client_secret = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return 'royalmail'


SETTINGS = RoyalMailSettings
