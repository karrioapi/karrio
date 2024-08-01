import django.db.models as models
import karrio.server.providers.models as providers


# @providers.has_rate_sheet("dpd")
class DPDSettings(providers.Carrier):
    class Meta:
        db_table = "dpd-settings"
        verbose_name = "DPD Settings"
        verbose_name_plural = "DPD Settings"

    delis_id = models.CharField(max_length=75)
    password = models.CharField(max_length=75)
    depot = models.CharField(max_length=25, null=True, blank=True)
    services = models.ManyToManyField("ServiceLevel", blank=True)
    account_country_code = models.CharField(
        max_length=3, blank=True, null=True, choices=providers.COUNTRIES
    )
    services = models.ManyToManyField("ServiceLevel", blank=True)

    @property
    def carrier_name(self) -> str:
        return "dpd"

    @property
    def default_services(self):
        import karrio.lib as lib
        from karrio.providers.dpd import units

        return lib.to_dict(
            units.DEFAULT_NL_SERVICES
            if self.account_country_code == "NL"
            else units.DEFAULT_SERVICES
        )


SETTINGS = DPDSettings
