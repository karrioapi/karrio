"""PurplShip CarrierName client settings."""

import attr
from purplship.domain.client import Client


@attr.s(auto_attribs=True)
class CarrierNameClient(Client):
    """CarrierName connection settings."""

    username: str
    password: str
    carrier_name: str = "CarrierName"
    server_url: str = "https://production/server"
