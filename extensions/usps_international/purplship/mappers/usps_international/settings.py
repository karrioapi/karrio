"""Purplship USPS International client settings."""

import attr
from purplship.providers.usps_international.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """USPS International connection settings."""

    # Carrier specific properties
    username: str
    password: str

    # Base properties
    id: str = None
    test: bool = False
    carrier_id: str = "usps_international"
