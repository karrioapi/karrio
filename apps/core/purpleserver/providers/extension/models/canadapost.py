from django.db import models
from purpleserver.providers.models.carrier import Carrier


class CanadaPostSettings(Carrier):
    CARRIER_NAME = 'canadapost'

    class Meta:
        db_table = "canada-post-settings"
        verbose_name = 'Canada Post Settings'
        verbose_name_plural = 'Canada Post Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    customer_number = models.CharField(max_length=200)
    contract_id = models.CharField(max_length=200, blank=True, default='')

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = CanadaPostSettings
