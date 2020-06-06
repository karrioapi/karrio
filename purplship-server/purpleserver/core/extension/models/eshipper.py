from django.db import models
from purpleserver.core.models.carrier import Carrier


class EShipperSettings(Carrier):
    class Meta:
        db_table = "eshipper-settings"
        verbose_name = 'eShipper Settings'
        verbose_name_plural = 'eShipper Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)


EShipperSettings._meta.get_field('carrier_id').default = 'eshipper'


def settings():
    return EShipperSettings
