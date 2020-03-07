"""PurplShip DHL client settings."""

import attr
from purplship.carriers.dhl.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """DHL connection settings."""

    site_id: str
    password: str
    carrier_name: str = "DHL Freight"
    server_url: str = "https://xmlpi-ea.dhl.com/XMLShippingServlet"

