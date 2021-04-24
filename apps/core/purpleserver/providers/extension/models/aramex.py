from django.db import models
from purpleserver.providers.models.carrier import Carrier


class AramexSettings(Carrier):
    CARRIER_NAME = 'aramex'

    class Meta:
        db_table = "aramex-settings"
        verbose_name = 'Aramex Settings'
        verbose_name_plural = 'Aramex Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    account_pin = models.CharField(max_length=200)
    account_entity = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
    account_country_code = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = AramexSettings
