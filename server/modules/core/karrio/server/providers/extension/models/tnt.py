from django.db import models
from karrio.server.providers.models.carrier import Carrier, COUNTRIES


class TNTSettings(Carrier):
    class Meta:
        db_table = "tnt-settings"
        verbose_name = 'TNT Settings'
        verbose_name_plural = 'TNT Settings'

    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100)
    account_country_code = models.CharField(max_length=3, blank=True, null=True, choices=COUNTRIES)

    @property
    def carrier_name(self) -> str:
        return 'tnt'


SETTINGS = TNTSettings
