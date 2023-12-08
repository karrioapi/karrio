import django.db.models as models
import karrio.lib as lib
import karrio.server.providers.models as providers


class BelgianPostSettings(providers.Carrier):
    class Meta:
        db_table = "bpost-settings"
        verbose_name = "Belgian Post Settings"
        verbose_name_plural = "Belgian Post Settings"

    account_id = models.CharField(max_length=100)
    passphrase = models.CharField(max_length=100)
    services = models.ManyToManyField("ServiceLevel", blank=True)

    @property
    def carrier_name(self) -> str:
        return "bpost"

    @property
    def default_services(self):
        from karrio.providers.bpost.units import DEFAULT_SERVICES

        return lib.to_dict(DEFAULT_SERVICES)


SETTINGS = BelgianPostSettings
