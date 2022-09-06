import karrio.lib as lib
import django.db.models as models
import karrio.server.providers.models as providers


class DPDHLSettings(providers.Carrier):
    class Meta:
        db_table = "dpdhl-settings"
        verbose_name = 'Deutsche Post DHL Settings'
        verbose_name_plural = 'Deutsche Post DHL Settings'

    app_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    signature = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100, blank=True, default='')
    services = models.ManyToManyField("ServiceLevel", blank=True)

    @property
    def carrier_name(self) -> str:
        return "dpdhl"

    @property
    def default_services(self):
        from karrio.mappers.dpdhl import units

        return lib.to_dict(units.DEFAULT_SERVICES)


SETTINGS = DPDHLSettings
