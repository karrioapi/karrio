"""PurplShip DHL client settings."""

import attr
from purplship.carriers.dhl.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """DHL connection settings."""

    carrier_name: str = "DHL"
    server_url: str = "https://xmlpi-ea.dhl.com/XMLShippingServlet"

