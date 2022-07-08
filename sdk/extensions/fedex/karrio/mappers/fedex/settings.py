"""Karrio FedEx client settings."""

import attr
from karrio.providers.fedex.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """FedEx connection settings."""

    password: str
    meter_number: str
    account_number: str
    user_key: str = None
    account_country_code: str = None

    id: str = None
    test_mode: bool = False
    carrier_id: str = "fedex"
    metadata: dict = {}

    @property
    def carrier_name(self):
        return "fedex"
