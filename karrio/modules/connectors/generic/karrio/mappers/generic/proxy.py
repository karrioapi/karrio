from karrio.api.proxy import Proxy as BaseProxy
from karrio.universal.mappers.rating_proxy import RatingMixinProxy
from karrio.universal.mappers.shipping_proxy import ShippingMixinProxy
from karrio.mappers.generic.settings import Settings


Proxy = type(
    "Proxy",
    (BaseProxy,),
    dict(
        settings=Settings,
        get_rates=RatingMixinProxy.get_rates,
        create_shipment=ShippingMixinProxy.create_shipment,
    ),
)
