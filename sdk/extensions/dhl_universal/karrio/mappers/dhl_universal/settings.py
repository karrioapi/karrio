"""Karrio DHL Universal settings."""

import attr
from karrio.providers.dhl_universal.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """DHL Universal connection settings."""

    # Carrier specific properties
    consumer_key: str
    consumer_secret: str

    # Base properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "dhl_universal"
    account_country_code: str = None
    metadata: dict = {}
