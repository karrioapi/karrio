"""Karrio FedEx client settings."""

import attr
from karrio.providers.fedex.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """FedEx connection settings."""

    password: str  # type:ignore
    meter_number: str  # type:ignore
    account_number: str  # type:ignore
    user_key: str = None
    language_code: str = "en"
    account_country_code: str = None

    id: str = None
    test_mode: bool = False
    carrier_id: str = "fedex"
    metadata: dict = {}

    @property
    def carrier_name(self):
        return "fedex"
