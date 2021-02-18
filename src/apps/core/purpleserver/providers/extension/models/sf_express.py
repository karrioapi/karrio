from django.db import models
from purpleserver.providers.models.carrier import Carrier


class SFExpressSettings(Carrier):
    CARRIER_NAME = 'sf_express'

    class Meta:
        db_table = "sf_express-settings"
        verbose_name = 'SF-Express Settings'
        verbose_name_plural = 'SF-Express Settings'

    partner_id = models.CharField(max_length=200)
    check_word = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = SFExpressSettings
