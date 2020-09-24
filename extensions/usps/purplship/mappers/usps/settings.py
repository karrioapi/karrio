"""PurplShip USPS client settings."""

import attr
from purplship.providers.usps.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """USPS connection settings."""

    username: str
    password: str
    id: str = None
    test: bool = False
    carrier_id: str = "usps"
