from django.db import models
from karrio.server.providers.models.carrier import Carrier


class FreightcomSettings(Carrier):
    CARRIER_NAME = "freightcom"

    class Meta:
        db_table = "freightcom-settings"
        verbose_name = "Freightcom Settings"
        verbose_name_plural = "Freightcom Settings"

    api_key = models.CharField(max_length=200, null=True)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = FreightcomSettings
