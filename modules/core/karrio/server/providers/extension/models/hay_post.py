import django.db.models as models

import karrio.server.providers.models.carrier as providers


class HayPostSettings(providers.Carrier):
    class Meta:
        db_table = "hay-post-settings"
        verbose_name = "Hay Post Settings"
        verbose_name_plural = "Hay Post Settings"

    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    customer_id = models.CharField(max_length=100)
    customer_type = models.CharField(max_length=100)

    @property
    def carrier_name(self) -> str:
        return "hay_post"


SETTINGS = HayPostSettings
