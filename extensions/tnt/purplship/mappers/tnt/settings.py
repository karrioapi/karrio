"""Purplship TNT settings."""

import attr
from purplship.providers.tnt.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """TNT connection settings."""

    # Carrier specific properties
    username: str
    password: str
    account_number: str = None
    account_country_code: str = None

    # Base properties
    id: str = None
    test: bool = False
    carrier_id: str = "tnt"
