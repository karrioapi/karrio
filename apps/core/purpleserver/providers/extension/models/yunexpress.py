from django.db import models
from purpleserver.providers.models.carrier import Carrier


class YunExpressSettings(Carrier):
    CARRIER_NAME = 'yunexpress'

    class Meta:
        db_table = "yunexpress-settings"
        verbose_name = 'Yunexpress Settings'
        verbose_name_plural = 'Yunexpress Settings'

    customer_number = models.CharField(max_length=200)
    api_secret = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = YunExpressSettings
