from purplship.core.utils import (
    Serializable,
    Deserializable,
)
from purplship.api.proxy import Proxy as BaseProxy
from purplship.universal.mappers.rating_proxy import RatingMixinProxy
from purplship.universal.mappers.shipping_proxy import ShippingMixinProxy
from purplship.mappers.generic.settings import Settings


class Proxy(ShippingMixinProxy, RatingMixinProxy, BaseProxy):
    settings: Settings

    def get_rates(self, request: Serializable) -> Deserializable:
        return super(RatingMixinProxy, self).get_rates(request)

    def create_shipment(self, request: Serializable) -> Deserializable:
        return super(ShippingMixinProxy, self).create_shipment(request)
