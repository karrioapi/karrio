"""Purplship DHL Universal settings."""

import attr
from purplship.providers.dhl_universal.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """DHL Universal connection settings."""

    # Carrier specific properties
    # username: str
    # password: str
    # account_number: str = None

    # Base properties
    id: str = None
    test: bool = False
    carrier_id: str = "dhl_universal"
