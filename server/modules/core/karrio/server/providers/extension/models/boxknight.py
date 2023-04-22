import django.db.models as models
import django.core.cache as caching

import karrio.lib as lib
import karrio.server.providers.models.carrier as providers


class BoxKnightSettings(providers.Carrier):
    class Meta:
        db_table = "boxknight-settings"
        verbose_name = "BoxKnight Settings"
        verbose_name_plural = "BoxKnight Settings"

    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    @property
    def carrier_name(self) -> str:
        return "boxknight"

    @property
    def cache(self):
        return lib.Cache(cache=caching.cache)


SETTINGS = BoxKnightSettings
