"""Karrio FedEx client settings."""

import attr
import jstruct
import karrio.lib as lib
from karrio.providers.fedex.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """FedEx connection settings."""

    api_key: str  # type:ignore
    secret_key: str  # type:ignore
    account_number: str = None

    cache: lib.Cache = jstruct.JStruct[lib.Cache]
    account_country_code: str = None
    carrier_id: str = "fedex"
    test_mode: bool = False
    metadata: dict = {}
    config: dict = {}
    id: str = None

    @property
    def carrier_name(self):
        return "fedex"
