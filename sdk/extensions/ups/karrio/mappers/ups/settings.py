"""Karrio UPS connection settings."""

import attr
import jstruct
import karrio.lib as lib
from karrio.providers.ups.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """UPS connection settings."""

    client_id: str  # type:ignore
    client_secret: str  # type:ignore
    account_number: str = None
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}

    id: str = None
    test_mode: bool = False
    carrier_id: str = "ups"
    cache: lib.Cache = jstruct.JStruct[lib.Cache, False, dict(default=lib.Cache())]
