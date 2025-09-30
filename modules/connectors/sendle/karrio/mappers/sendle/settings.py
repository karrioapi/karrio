"""Karrio Sendle client settings."""

import attr
import karrio.providers.sendle.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Sendle connection settings."""

    # required carrier specific properties
    sendle_id: str
    api_key: str

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "sendle"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
