import typing
import django.db.models as models
import karrio.server.providers.models.carrier as carrier


class TGESettings(carrier.Carrier):
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
    my_toll_token = models.CharField(max_length=250)
    my_toll_identity = models.CharField(max_length=100)
    account_code = models.CharField(max_length=100)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME

    @property
    def sssc_count(self) -> typing.Optional[int]:
        meta = getattr(self.carrier_shipments.first(), "meta", {})
        return meta.get("sssc_count")

    @property
    def shipment_count(self) -> typing.Optional[int]:
        meta = getattr(self.carrier_shipments.first(), "meta", {})
        return meta.get("shipment_count")


SETTINGS = TGESettings
