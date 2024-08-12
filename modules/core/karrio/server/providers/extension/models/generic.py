import django.db.models as models
import django.core.validators as validators
import karrio.server.providers.models as providers


# @providers.has_rate_sheet("generic")
class GenericSettings(providers.Carrier):
    CARRIER_NAME = "generic"

    class Meta:
        db_table = "generic-settings"
        verbose_name = "Custom Carrier Settings"
        verbose_name_plural = "Custom Carrier Settings"

    display_name = models.CharField(max_length=30, help_text="Carrier display name")
    custom_carrier_name = models.CharField(
        max_length=30,
        validators=[validators.RegexValidator(r"^[a-z0-9_]+$")],
        help_text="Unique carrier slug, lowercase alphanumeric characters and underscores only",
    )
    label_template = models.OneToOneField(
        "LabelTemplate", null=True, blank=True, on_delete=models.CASCADE
    )
    account_number = models.CharField(max_length=20, null=True, blank=True, default="")
    account_country_code = models.CharField(
        max_length=3, null=True, blank=True, choices=providers.COUNTRIES
    )
    services = models.ManyToManyField("ServiceLevel", blank=True)

    @property
    def carrier_name(self) -> str:
        return self.custom_carrier_name  # "generic"


SETTINGS = GenericSettings
