"""Karrio AmazonMws connection settings."""

import attr
from karrio.providers.amazon_mws.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """AmazonMws connection settings."""

    id: str = None
    test: bool = False
    carrier_id: str = "amazon_mws"
    account_country_code: str = None
