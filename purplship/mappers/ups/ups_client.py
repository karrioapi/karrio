"""PurplShip UPS client settings."""

import attr
from purplship.domain.client import Client


@attr.s(auto_attribs=True)
class UPSClient(Client):
    """UPS connection settings."""

    username: str
    password: str
    access_license_number: str
    carrier_name: str = "UPS"
    server_url: str = "https://onlinetools.ups.com/webservices"
