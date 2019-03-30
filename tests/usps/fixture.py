import purplship
from purplship.mappers.usps import USPSProxy

proxy: USPSProxy = purplship.gateway["usps"].create(
    {
        "server_url": "http://production.shippingapis.com/ShippingAPI.dll",
        "username": "username",
        "password": "password",
    }
)
