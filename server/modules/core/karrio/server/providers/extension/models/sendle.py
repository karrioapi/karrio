from django.db import models
from karrio.server.providers.models.carrier import Carrier


class SendleSettings(Carrier):
    class Meta:
        db_table = "sendle-settings"
        verbose_name = 'Sendle Settings'
        verbose_name_plural = 'Sendle Settings'

    sendle_id = models.CharField(max_length=200)
    api_key = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return 'sendle'


SETTINGS = SendleSettings
