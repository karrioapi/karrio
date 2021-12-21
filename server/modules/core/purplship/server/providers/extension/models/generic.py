from django.db import models
from purplship.core.utils import DP
from purplship.server.providers.models.carrier import Carrier, COUNTRIES


class GenericSettings(Carrier):
    class Meta:
        db_table = "generic-settings"
        verbose_name = "Custom Carrier Settings"
        verbose_name_plural = "Custom Carrier Settings"

    services = models.ManyToManyField("ServiceLevel", blank=True)
    label_template = models.ForeignKey(
        "LabelTemplate", null=True, on_delete=models.CASCADE
    )
    account_country_code = models.CharField(
        max_length=3, null=True, blank=True, choices=COUNTRIES
    )

    @property
    def carrier_name(self) -> str:
        return "generic"

    @property
    def default_services(self):
        from purplship.mappers.generic import DEFAULT_SERVICES

        return DP.to_dict(DEFAULT_SERVICES)


SETTINGS = GenericSettings
