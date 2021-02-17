"""Purplship Sendle settings."""

import attr
from purplship.providers.sendle.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Sendle connection settings."""

    # Carrier specific properties
    sendle_id: str
    api_key: str

    # Base properties
    id: str = None
    test: bool = False
    carrier_id: str = "sendle"
