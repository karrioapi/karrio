"""PurplShip Sendle client settings."""

import attr
from purplship.carriers.sendle.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Sendle connection settings."""

    sendle_id: str
    api_key: str
    id: str = None
    carrier_name: str = "Sendle"
    server_url: str = "https://api.sendle.com"
