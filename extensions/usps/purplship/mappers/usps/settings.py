"""Purplship USPS client settings."""

import attr
from purplship.providers.usps.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """USPS connection settings."""

    # Carrier specific properties
    username: str
    password: str

    # Base properties
    id: str = None
    test: bool = False
    carrier_id: str = "usps"
