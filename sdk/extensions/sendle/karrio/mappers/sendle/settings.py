"""Karrio Sendle settings."""

import attr
from karrio.providers.sendle.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Sendle connection settings."""

    # Carrier specific properties
    sendle_id: str
    api_key: str

    # Base properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "sendle"
    account_country_code: str = "AU"
    metadata: dict = {}
