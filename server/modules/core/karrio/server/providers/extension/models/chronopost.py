from django.db import models
from karrio.server.providers.models.carrier import Carrier, COUNTRIES


class ChronopostSettings(Carrier):
    class Meta:
        db_table = "chronopost-settings"
        verbose_name = 'Chronopost Settings'
        verbose_name_plural = 'Chronopost Settings'

    password = models.CharField(max_length=50)
    account_number = models.CharField(max_length=50, blank=True, default='')
    account_country_code = models.CharField(max_length=3, blank=True, null=True, choices=COUNTRIES)

    @property
    def carrier_name(self) -> str:
        return 'chronopost'


SETTINGS = ChronopostSettings
