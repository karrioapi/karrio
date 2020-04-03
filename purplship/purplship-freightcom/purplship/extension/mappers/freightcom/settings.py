"""PurplShip freightcom connection settings."""

import attr
from purplship.extension.carriers.freightcom.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Freightcom connection settings."""

    username: str
    password: str
    carrier_name: str = "Freightcom"
    server_url: str = "https://app.freightcom.com/rpc2"
