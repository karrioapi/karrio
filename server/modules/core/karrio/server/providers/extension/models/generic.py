from django.db import models
from django.core.validators import RegexValidator
from karrio.core.utils import DP
from karrio.server.providers.models.carrier import Carrier, COUNTRIES


class GenericSettings(Carrier):
    class Meta:
        db_table = "generic-settings"
        verbose_name = "Custom Carrier Settings"
        verbose_name_plural = "Custom Carrier Settings"

    display_name = models.CharField(max_length=50, help_text="Carrier display name")
    custom_carrier_name = models.CharField(
        max_length=50,
        validators=[RegexValidator(r"^[a-z0-9_]+$")],
        help_text="Unique carrier slug, lowercase alphanumeric characters and underscores only",
    )
    services = models.ManyToManyField("ServiceLevel", blank=True)
    label_template = models.OneToOneField(
        "LabelTemplate", null=True, blank=True, on_delete=models.CASCADE
    )
    account_number = models.CharField(max_length=25, blank=True)
    account_country_code = models.CharField(
        max_length=3, null=True, blank=True, choices=COUNTRIES
    )

    @property
    def carrier_name(self) -> str:
        return self.custom_carrier_name  # "generic"

    @property
    def default_services(self):
        from karrio.mappers.generic import DEFAULT_SERVICES

        return DP.to_dict(DEFAULT_SERVICES)


SETTINGS = GenericSettings
