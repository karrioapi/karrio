"""Karrio Royal Mail settings."""

import attr
from karrio.providers.royalmail.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Royal Mail connection settings."""

    # Carrier specific properties
    client_id: str
    client_secret: str

    # Base properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "royalmail"
    account_country_code: str = "UK"
    metadata: dict = {}
    config: dict = {}
