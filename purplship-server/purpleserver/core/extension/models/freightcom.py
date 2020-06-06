from django.db import models
from purpleserver.core.models.carrier import Carrier


class FreightcomSettings(Carrier):
    class Meta:
        db_table = "freightcom-settings"
        verbose_name = 'Freightcom Settings'
        verbose_name_plural = 'Freightcom Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)


FreightcomSettings._meta.get_field('carrier_id').default = 'freightcom'


def settings():
    return FreightcomSettings
