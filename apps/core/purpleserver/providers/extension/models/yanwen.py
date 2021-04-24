from django.db import models
from purpleserver.providers.models.carrier import Carrier


class YanwenSettings(Carrier):
    CARRIER_NAME = 'yanwen'

    class Meta:
        db_table = "yanwen-settings"
        verbose_name = 'Yanwen Settings'
        verbose_name_plural = 'Yanwen Settings'

    customer_number = models.CharField(max_length=200)
    license_key = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = YanwenSettings
