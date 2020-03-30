"""PurplShip USPS client settings."""

import attr
from purplship.carriers.usps.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """USPS connection settings."""

    username: str
    password: str
    id: str = None
    carrier_name: str = "USPS"
    server_url: str = "https://secure.shippingapis.com/ShippingAPI.dll"
