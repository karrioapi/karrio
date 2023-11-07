import django.db.models as models

import karrio.server.providers.models.carrier as providers


class GEODISSettings(providers.Carrier):
    class Meta:
        db_table = "geodis-settings"
        verbose_name = "GEODIS Settings"
        verbose_name_plural = "GEODIS Settings"

    api_key = models.CharField(max_length=100)
    identifier = models.CharField(max_length=50)
    code_client = models.CharField(max_length=50)
    language = models.CharField(max_length=10, null=True, default="fr")

    @property
    def carrier_name(self) -> str:
        return "geodis"


SETTINGS = GEODISSettings
