"""Karrio FedEx client settings."""

import attr
import karrio.providers.fedex.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """FedEx connection settings."""

    api_key: str = None
    # api_key: str = attr.ib(default=None, metadata={"sensitive": True})
    secret_key: str = None
    # secret_key: str = attr.ib(default=None, metadata={"sensitive": True})
    account_number: str = None
    track_api_key: str = None
    # track_api_key: str = attr.ib(default=None, metadata={"sensitive": True})
    track_secret_key: str = None
    # track_secret_key: str = attr.ib(default=None, metadata={"sensitive": True})

    account_country_code: str = None
    carrier_id: str = "fedex"
    test_mode: bool = False
    metadata: dict = {}
    config: dict = {}
    id: str = None
