"""Karrio Canada post client settings."""

import attr
from karrio.providers.canadapost import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Canada post connection settings."""

    username: str
    password: str
    customer_number: str = None
    contract_id: str = None
    language: str = "en"

    id: str = None
    test_mode: bool = False
    carrier_id: str = "canadapost"
    account_country_code: str = "CA"
    metadata: dict = {}
