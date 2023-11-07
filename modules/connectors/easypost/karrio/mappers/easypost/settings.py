"""Karrio EasyPost connection settings."""

import attr
from karrio.providers.easypost.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """EasyPost connection settings."""

    api_key: str

    id: str = None
    test_mode: bool = False
    carrier_id: str = "easypost"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
