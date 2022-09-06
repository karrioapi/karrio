from django.db import models
from karrio.server.providers.models.carrier import Carrier


class USPSInternationalSettings(Carrier):
    class Meta:
        db_table = "usps_international-settings"
        verbose_name = 'USPS International Settings'
        verbose_name_plural = 'USPS International Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    mailer_id = models.CharField(max_length=200, null=True, blank=True)
    customer_registration_id = models.CharField(max_length=200, blank=True, null=True)
    logistics_manager_mailer_id = models.CharField(max_length=200, blank=True, null=True)

    @property
    def carrier_name(self) -> str:
        return 'usps_international'


SETTINGS = USPSInternationalSettings
