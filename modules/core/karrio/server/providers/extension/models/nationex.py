import django.db.models as models

import karrio.server.providers.models.carrier as providers


class NationexSettings(providers.Carrier):
    class Meta:
        db_table = "nationex-settings"
        verbose_name = "Nationex Settings"
        verbose_name_plural = "Nationex Settings"

    api_key = models.CharField(max_length=100)
    customer_id = models.CharField(max_length=50)
    billing_account = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=10, null=True, default="en")

    @property
    def carrier_name(self) -> str:
        return "nationex"


SETTINGS = NationexSettings
