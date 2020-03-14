"""PurplShip DHL client settings."""

import attr
from purplship.carriers.dhl.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """DHL connection settings."""

    site_id: str
    password: str
    account_number: str = None
    carrier_name: str = "DHL"
    server_url: str = "https://xmlpi-ea.dhl.com/XMLShippingServlet"
