"""Karrio ParcelOne client settings."""

import attr
import typing
import karrio.providers.parcelone.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """ParcelOne connection settings."""

    # Required credentials
    username: str
    password: str
    mandator_id: str
    consigner_id: str

    # Generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "parcelone"
    account_country_code: str = "DE"
    metadata: dict = {}
    config: dict = {}
