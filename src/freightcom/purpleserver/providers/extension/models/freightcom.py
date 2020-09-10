from django.db import models
from purpleserver.providers.models.carrier import Carrier


class FreightcomSettings(Carrier):
    CARRIER_NAME = 'freightcom'

    class Meta:
        db_table = "freightcom-settings"
        verbose_name = 'Freightcom Settings'
        verbose_name_plural = 'Freightcom Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)


def settings():
    return FreightcomSettings
