"""Karrio Zoom2u client settings."""

import attr
import karrio.providers.zoom2u.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Zoom2u connection settings."""

    # required carrier specific properties
    api_key: str

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "zoom2u"
    account_country_code: str = "AU"
    metadata: dict = {}
    config: dict = {}
