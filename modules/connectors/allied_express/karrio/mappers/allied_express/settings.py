"""Karrio Allied Express client settings."""

import attr
import karrio.providers.allied_express.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Allied Express connection settings."""

    # required carrier specific properties
    username: str
    password: str
    account: str = None
    service_type: str = "R"

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "allied_express"
    account_country_code: str = "AU"
    metadata: dict = {}
    config: dict = {}
