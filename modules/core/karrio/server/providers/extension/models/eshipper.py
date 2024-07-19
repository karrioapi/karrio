import django.db.models as models
import karrio.server.providers.models as providers


class EShipperSettings(providers.Carrier):
    CARRIER_NAME = "eshipper"

    class Meta:
        db_table = "eshipper-settings"
        verbose_name = "eShipper Settings"
        verbose_name_plural = "eShipper Settings"

    principal = models.CharField(max_length=100)
    credential = models.CharField(max_length=100)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = EShipperSettings
