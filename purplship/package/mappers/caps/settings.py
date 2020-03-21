"""PurplShip Canada post client settings."""

import attr
from purplship.carriers.caps import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Canada post connection settings."""

    username: str
    password: str
    customer_number: str
    contract_id: str = None
    carrier_name: str = "CanadaPost"
    server_url: str = "https://soagw.canadapost.ca"
