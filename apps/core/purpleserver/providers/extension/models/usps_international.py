from django.db import models
from purpleserver.providers.models.carrier import Carrier


class USPSInternationalSettings(Carrier):
    CARRIER_NAME = 'usps_international'

    class Meta:
        db_table = "usps_international-settings"
        verbose_name = 'USPS International Settings'
        verbose_name_plural = 'USPS International Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    mailer_id = models.CharField(max_length=200, null=True)
    customer_registration_id = models.CharField(max_length=200, null=True)
    logistics_manager_mailer_id = models.CharField(max_length=200, null=True)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = USPSInternationalSettings
