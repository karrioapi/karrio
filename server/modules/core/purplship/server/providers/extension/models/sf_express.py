from django.db import models
from karrio.server.providers.models.carrier import Carrier


class SFExpressSettings(Carrier):
    class Meta:
        db_table = "sf_express-settings"
        verbose_name = 'SF-Express Settings'
        verbose_name_plural = 'SF-Express Settings'

    partner_id = models.CharField(max_length=200)
    check_word = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return 'sf_express'


SETTINGS = SFExpressSettings
