"""Karrio Canpar client settings."""

import attr
from karrio.providers.canpar import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Canpar connection settings."""

    username: str
    password: str
    language: str = "en"

    id: str = None
    test_mode: bool = False
    carrier_id: str = "canpar"
    account_country_code: str = "CA"
    metadata: dict = {}
