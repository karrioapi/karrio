"""PurplShip Sendle client settings."""

import attr
from purplship.domain.client import Client


@attr.s(auto_attribs=True)
class SendleClient(Client):
    """Sendle connection settings."""

    sendle_id: str
    api_key: str
    carrier_name: str = "Sendle"
    server_url: str = "https://api.sendle.com"
