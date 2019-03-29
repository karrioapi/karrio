"""PurplShip USPS client settings."""

import attr
from purplship.domain.client import Client


@attr.s(auto_attribs=True)
class USPSClient(Client):
    """USPS connection settings."""

    username: str
    password: str
    carrier_name: str = "USPS"
    server_url: str = "https://secure.shippingapis.com/ShippingAPI.dll"
