"""PurplShip FedEx client settings."""

import attr
from purplship.domain.client import Client


@attr.s(auto_attribs=True)
class FedexClient(Client):
    """FedEx connection settings."""

    user_key: str
    password: str
    meter_number: str
    account_number: str
    carrier_name: str = "Fedex"
    server_url: str = "https://ws.fedex.com:443/web-services"
