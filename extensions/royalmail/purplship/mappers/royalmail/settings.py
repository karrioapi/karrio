"""Purplship Royal Mail settings."""

import attr
from purplship.providers.royalmail.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Royal Mail connection settings."""

    # Carrier specific properties
    client_id: str
    client_secret: str

    # Base properties
    id: str = None
    test: bool = False
    carrier_id: str = "royalmail"
