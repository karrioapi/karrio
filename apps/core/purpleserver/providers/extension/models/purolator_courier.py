from django.db import models
from purpleserver.providers.models.carrier import Carrier


class PurolatorCourierSettings(Carrier):
    CARRIER_NAME = 'purolator_courier'

    class Meta:
        db_table = "purolator_courier-settings"
        verbose_name = 'Purolator Courier Settings'
        verbose_name_plural = 'Purolator Courier Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
    user_token = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = PurolatorCourierSettings
