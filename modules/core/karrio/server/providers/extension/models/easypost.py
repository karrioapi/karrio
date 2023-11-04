from django.db import models
from karrio.server.providers.models.carrier import Carrier


class EasyPostSettings(Carrier):
    CARRIER_NAME = "easypost"

    class Meta:
        db_table = "easypost-settings"
        verbose_name = "EasyPost Settings"
        verbose_name_plural = "EasyPost Settings"

    api_key = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = EasyPostSettings
