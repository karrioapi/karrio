from purplship.core.utils import (
    Serializable,
    Deserializable,
)
from purplship.api.proxy import Proxy as BaseProxy
from purplship.universal.mappers import ShippingMixinProxy, RatingMixinProxy
from purplship.mappers.generic.settings import Settings


class Proxy(ShippingMixinProxy, RatingMixinProxy, BaseProxy):
    settings: Settings

    def get_rates(self, request: Serializable) -> Deserializable:
        return super().get_rates(request)

    def create_shipment(self, request: Serializable) -> Deserializable:
        return super().create_shipment(request)
