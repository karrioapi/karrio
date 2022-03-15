from django.db import models
from karrio.core.utils import DP
from karrio.server.providers.models.carrier import Carrier


class DHLPolandSettings(Carrier):
    class Meta:
        db_table = "dhl-poland-settings"
        verbose_name = "DHL Poland Settings"
        verbose_name_plural = "DHL Poland Settings"

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200, blank=True)
    services = models.ManyToManyField("ServiceLevel", blank=True)

    @property
    def carrier_name(self) -> str:
        return "dhl_poland"

    @property
    def default_services(self):
        from karrio.mappers.dhl_poland import DEFAULT_SERVICES

        return DP.to_dict(DEFAULT_SERVICES)


SETTINGS = DHLPolandSettings
