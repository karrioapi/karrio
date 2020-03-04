"""PurplShip FedEx client settings."""

import attr
from purplship.carriers.fedex.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """FedEx connection settings."""

    carrier_name: str = "FedEx"
    server_url: str = "https://ws.fedex.com:443/web-services"
