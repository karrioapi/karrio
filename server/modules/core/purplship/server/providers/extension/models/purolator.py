from django.db import models
from karrio.server.providers.models.carrier import Carrier


class PurolatorSettings(Carrier):
    class Meta:
        db_table = "purolator-settings"
        verbose_name = 'Purolator Settings'
        verbose_name_plural = 'Purolator Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
    user_token = models.CharField(max_length=200, null=True)

    @property
    def carrier_name(self) -> str:
        return 'purolator'


SETTINGS = PurolatorSettings
