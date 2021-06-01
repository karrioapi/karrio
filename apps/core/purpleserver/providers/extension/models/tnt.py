from django.db import models
from purpleserver.providers.models.carrier import Carrier


class TNTSettings(Carrier):
    CARRIER_NAME = 'tnt'

    class Meta:
        db_table = "tnt-settings"
        verbose_name = 'TNT Settings'
        verbose_name_plural = 'TNT Settings'

    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100)
    account_country_code = models.CharField(max_length=3)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = TNTSettings
