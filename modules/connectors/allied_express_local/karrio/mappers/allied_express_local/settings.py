"""Karrio Allied Express Local client settings."""

import attr
import karrio.providers.allied_express_local.utils as utils


@attr.s(auto_attribs=True)
class Settings(utils.Settings):
    """Allied Express Local connection settings."""

    # required carrier specific properties
    username: str
    password: str
    account: str = None
    service_type: utils.AlliedServiceType = "R"  # type: ignore

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "allied_express_local"
    account_country_code: str = "AU"
    metadata: dict = {}
    config: dict = {}
