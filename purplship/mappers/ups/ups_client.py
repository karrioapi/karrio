"""PurplShip UPS client settings."""

import attr
from purplship.domain.client import Client
from enum import Enum


class UPSApi(Enum):
    Freight = "Freight"
    Package = "Package"


@attr.s(auto_attribs=True)
class UPSClient(Client):
    """UPS connection settings."""

    username: str
    password: str
    access_license_number: str
    carrier_name: str = "UPS"
    server_url: str = "https://onlinetools.ups.com/webservices"
    api: str = UPSApi.Package.name
