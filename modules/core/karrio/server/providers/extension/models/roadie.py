import django.db.models as models
import karrio.server.providers.models.carrier as providers


class RoadieSettings(providers.Carrier):
    class Meta:
        db_table = "roadie-settings"
        verbose_name = "Roadie Settings"
        verbose_name_plural = "Roadie Settings"

    api_key = models.CharField(max_length=100)

    @property
    def carrier_name(self) -> str:
        return "roadie"


SETTINGS = RoadieSettings
