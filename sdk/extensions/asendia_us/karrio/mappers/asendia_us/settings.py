"""Karrio Asendia US client settings."""

import attr
import karrio.providers.asendia_us.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Asendia US connection settings."""

    # required carrier specific properties
    username: str  # type: ignore
    password: str  # type: ignore
    api_key: str  # type: ignore
    account_number: str = None

    # generic properties
    carrier_id: str = "asendia_us"
    account_country_code: str = "US"
    test_mode: bool = False
    metadata: dict = {}
    config: dict = {}
    id: str = None
