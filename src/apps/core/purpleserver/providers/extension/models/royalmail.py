from django.db import models
from purpleserver.providers.models.carrier import Carrier


class RoyalMailSettings(Carrier):
    CARRIER_NAME = 'royalmail'

    class Meta:
        db_table = "royalmail-settings"
        verbose_name = 'Royal Mail Settings'
        verbose_name_plural = 'Royal Mail Settings'

    client_id = models.CharField(max_length=200)
    client_secret = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = RoyalMailSettings
