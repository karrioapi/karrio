from django.db import models
from purpleserver.providers.models.carrier import Carrier


class USPSSettings(Carrier):
    CARRIER_NAME = 'usps'

    class Meta:
        db_table = "usps-settings"
        verbose_name = 'USPS Settings'
        verbose_name_plural = 'USPS Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    mailer_id = models.CharField(max_length=200, null=True)
    customer_registration_id = models.CharField(max_length=200, null=True)
    logistics_manager_mailer_id = models.CharField(max_length=200, null=True)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = USPSSettings
