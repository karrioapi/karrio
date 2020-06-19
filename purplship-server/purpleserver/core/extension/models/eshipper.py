from django.db import models
from purpleserver.core.models.carrier import Carrier


class EShipperSettings(Carrier):
    CARRIER_NAME = 'eshipper'

    class Meta:
        db_table = "eshipper-settings"
        verbose_name = 'eShipper Settings'
        verbose_name_plural = 'eShipper Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)


def settings():
    return EShipperSettings
