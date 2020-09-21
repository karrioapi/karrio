"""Purplship Canada post client settings."""

import attr
from purplship.providers.canadapost import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Canada post connection settings."""

    username: str
    password: str
    customer_number: str
    contract_id: str = None
    language: str = "en"
    id: str = None
    test: bool = False
    carrier_id: str = "canadapost"
