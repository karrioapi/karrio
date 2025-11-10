"""Karrio Teleship client settings."""

import attr
import karrio.providers.teleship.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Teleship connection settings."""

    # Add carrier specific API connection properties here
    api_key: str
    account_number: str = None

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "teleship"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
