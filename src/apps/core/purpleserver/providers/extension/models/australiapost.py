from django.db import models
from purpleserver.providers.models.carrier import Carrier


class AustraliaPostSettings(Carrier):
    CARRIER_NAME = 'australiapost'

    class Meta:
        db_table = "australia-post-settings"
        verbose_name = 'Australia Post Settings'
        verbose_name_plural = 'Australia Post Settings'

    api_key = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = AustraliaPostSettings
