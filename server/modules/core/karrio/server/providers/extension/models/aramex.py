from django.db import models
from karrio.server.providers.models.carrier import Carrier, COUNTRIES


class AramexSettings(Carrier):
    class Meta:
        db_table = "aramex-settings"
        verbose_name = 'Aramex Settings'
        verbose_name_plural = 'Aramex Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    account_pin = models.CharField(max_length=200)
    account_entity = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
    account_country_code = models.CharField(max_length=3, blank=True, null=True, choices=COUNTRIES)

    @property
    def carrier_name(self) -> str:
        return 'aramex'


SETTINGS = AramexSettings
