import typing
import django.db.models as models
import django.core.cache as caching
import karrio.server.providers.models as providers


class TGESettings(providers.Carrier):
    CARRIER_NAME = "tge"

    class Meta:
        db_table = "tge-settings"
        verbose_name = "TGE Settings"
        verbose_name_plural = "TGE Settings"

    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100)
    toll_username = models.CharField(max_length=100)
    toll_password = models.CharField(max_length=100)
    my_toll_token = models.TextField(max_length=None)
    my_toll_identity = models.CharField(max_length=100)
    account_code = models.CharField(max_length=100)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME

    @property
    def sscc_count(self) -> typing.Optional[int]:
        cache_key = f"{self.carrier_name}|{self.api_key}"
        state = caching.cache.get(cache_key) or {}

        if state.get("sscc_count") is not None:
            return state["sscc_count"]

        meta = getattr(self.carrier_shipments.first(), "meta", {})

        if meta.get("sscc_count") is not None:
            state["sscc_count"] = meta["sscc_count"]
            caching.cache.set(cache_key, state)
            return meta["sscc_count"]

        return None

    @property
    def shipment_count(self) -> typing.Optional[int]:
        cache_key = f"{self.carrier_name}|{self.api_key}"
        state = caching.cache.get(cache_key) or {}

        if state.get("shipment_count") is not None:
            return state["shipment_count"]

        meta = getattr(self.carrier_shipments.first(), "meta", {})

        if meta.get("shipment_count") is not None:
            state["shipment_count"] = meta["shipment_count"]
            caching.cache.set(cache_key, state)
            return meta["shipment_count"]

        return None


SETTINGS = TGESettings
