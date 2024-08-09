from django.db import models
from karrio.server.providers.models.carrier import Carrier


class USPSWTInternationalSettings(Carrier):
    class Meta:
        db_table = "usps_wt_international-settings"
        verbose_name = "USPS Web Tools International Settings"
        verbose_name_plural = "USPS Web Tools International Settings"

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    mailer_id = models.CharField(max_length=200, null=True, blank=True)
    customer_registration_id = models.CharField(max_length=200, blank=True, null=True)
    logistics_manager_mailer_id = models.CharField(
        max_length=200, blank=True, null=True
    )

    @property
    def carrier_name(self) -> str:
        return "usps_wt_international"


SETTINGS = USPSWTInternationalSettings
