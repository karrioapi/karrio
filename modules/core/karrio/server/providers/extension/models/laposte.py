import django.db.models as models
import karrio.server.providers.models.carrier as providers


class LaPosteSettings(providers.Carrier):
    class Meta:
        db_table = "laposte-settings"
        verbose_name = "LaPoste Settings"
        verbose_name_plural = "LaPoste Settings"

    api_key = models.CharField(max_length=100)
    lang = models.CharField(max_length=10, null=True, default="fr_FR")

    @property
    def carrier_name(self) -> str:
        return "laposte"


SETTINGS = LaPosteSettings
