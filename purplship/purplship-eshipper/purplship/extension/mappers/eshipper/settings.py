"""PurplShip eshipper connection settings."""

import attr
from purplship.extension.carriers.eshipper.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """eshipper connection settings."""

    username: str
    password: str
    carrier_name: str = "eshipper"
    server_url: str = "http://web.eshipper.com/rpc2"
