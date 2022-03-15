from django.db import models
from karrio.server.providers.models.carrier import Carrier


class CanadaPostSettings(Carrier):
    class Meta:
        db_table = "canada-post-settings"
        verbose_name = 'Canada Post Settings'
        verbose_name_plural = 'Canada Post Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    customer_number = models.CharField(max_length=200, blank=True)
    contract_id = models.CharField(max_length=200, blank=True)

    @property
    def carrier_name(self) -> str:
        return 'canadapost'


SETTINGS = CanadaPostSettings
