"""Purplship Canpar client settings."""

import attr
from purplship.providers.canpar import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Canpar connection settings."""

    username: str
    password: str
    id: str = None
    test: bool = False
    carrier_id: str = "canpar"
