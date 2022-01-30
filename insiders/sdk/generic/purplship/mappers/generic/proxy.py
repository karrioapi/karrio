from purplship.core.utils import (
    Serializable,
    Deserializable,
)
from purplship.api.proxy import Proxy as BaseProxy
from purplship.universal.mappers.rating_proxy import RatingMixinProxy
from purplship.universal.mappers.shipping_proxy import ShippingMixinProxy
from purplship.mappers.generic.settings import Settings


Proxy = type(
    "Proxy",
    (BaseProxy,),
    dict(
        settings=Settings,
        get_rates=RatingMixinProxy.get_rates,
        create_shipment=ShippingMixinProxy.create_shipment,
    ),
)
