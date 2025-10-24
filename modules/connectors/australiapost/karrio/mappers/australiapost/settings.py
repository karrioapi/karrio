"""Karrio Australia Post client settings."""

import attr
import karrio.providers.australiapost.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Australia Post connection settings."""

    # required carrier specific properties
    api_key: str
    password: str
    account_number: str

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "australiapost"
    account_country_code: str = "AU"
    metadata: dict = {}
    config: dict = {}
