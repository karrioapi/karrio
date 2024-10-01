"""Karrio TNT Connect Italy client settings."""

import attr
import karrio.providers.tnt_it.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """TNT Connect Italy connection settings."""

    # Add carrier specific API connection properties here
    customer: str
    username: str
    password: str
    account_number: str = None

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "tnt_it"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
