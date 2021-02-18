from django.db import models
from purpleserver.providers.models.carrier import Carrier


class SendleSettings(Carrier):
    CARRIER_NAME = 'sendle'

    class Meta:
        db_table = "sendle-settings"
        verbose_name = 'Sendle Settings'
        verbose_name_plural = 'Sendle Settings'

    sendle_id = models.CharField(max_length=200)
    api_key = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = SendleSettings
