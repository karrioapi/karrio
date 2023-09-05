"""Karrio Asendia US client settings."""

import attr
import karrio.providers.asendia_us.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Asendia US connection settings."""

    # required carrier specific properties
    username: str
    password: str
    x_asendia_one_api_key: str
    account_number: str = None

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "asendia_us"
    account_country_code: str = "US"
    metadata: dict = {}
