"""PurplShip UPS connection settings."""

import attr
from purplship.carriers.ups.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """UPS connection settings."""

    username: str
    password: str
    access_license_number: str
    carrier_name: str = "UPS Freight"
    server_url: str = "https://onlinetools.ups.com/webservices"
