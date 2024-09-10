"""Karrio Ninja Van client settings."""

import attr
from karrio.providers.ninja_van.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Ninja Van connection settings."""

    # required carrier specific properties
    client_id: str = None
    client_secret: str = None

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "ninja_van"
    account_country_code: str = "SG"
    metadata: dict = {}
    config: dict = {}
