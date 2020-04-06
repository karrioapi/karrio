"""PurplShip UPS connection settings."""

import attr
from purplship.carriers.purolator.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """UPS connection settings."""

    username: str
    password: str
    account_number: str
    user_token: str = None
    language: str = "en"
    id: str = None
    test: bool = False
    carrier_name: str = "Purolator"
