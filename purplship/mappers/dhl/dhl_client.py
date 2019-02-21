"""PurplShip DHL client settings."""

import attr
from purplship.domain.client import Client


@attr.s(auto_attribs=True)
class DHLClient(Client):
    """DHL connection settings."""

    site_id: str
    password: str
    carrier_name: str = "DHL"
    server_url: str = "https://xmlpi-ea.dhl.com/XMLShippingServlet"
