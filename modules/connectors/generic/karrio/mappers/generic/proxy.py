from karrio.api.proxy import Proxy as BaseProxy
from karrio.mappers.generic.settings import Settings
from karrio.universal.mappers.rating_proxy import RatingMixinProxy
from karrio.universal.mappers.shipping_proxy import ShippingMixinProxy

Proxy = type(
    "Proxy",
    (BaseProxy,),
    dict(
        settings=Settings,
        get_rates=RatingMixinProxy.get_rates,
        create_shipment=ShippingMixinProxy.create_shipment,
    ),
)
