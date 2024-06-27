"""Karrio DHL Express client settings."""

import attr
import karrio.providers.mydhl.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """DHL Express connection settings."""

    # required carrier specific properties
    username: str
    password: str
    api_key: str
    account_number: str = None

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "mydhl"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
