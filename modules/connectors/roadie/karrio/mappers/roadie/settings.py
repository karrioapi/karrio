"""Karrio Roadie client settings."""

import attr
import karrio.providers.roadie.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Roadie connection settings."""

    # required carrier specific properties
    api_key: str

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "roadie"
    account_country_code: str = "US"
    metadata: dict = {}
    config: dict = {}
