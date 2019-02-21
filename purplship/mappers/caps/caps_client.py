"""PurplShip Canada post client settings."""

import attr
from purplship.domain.client import Client


@attr.s(auto_attribs=True)
class CanadaPostClient(Client):
    """Canada post connection settings."""

    username: str
    password: str
    customer_number: str
    carrier_name: str = "CanadaPost"
    server_url: str = "https://soagw.canadapost.ca"
