from django.db import models
from karrio.server.providers.models.carrier import Carrier


class Zoom2uSettings(Carrier):
    CARRIER_NAME = "zoom2u"

    class Meta:
        db_table = "zoom2u-settings"
        verbose_name = "Zoom2u Settings"
        verbose_name_plural = "Zoom2u Settings"

    api_key = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = Zoom2uSettings
