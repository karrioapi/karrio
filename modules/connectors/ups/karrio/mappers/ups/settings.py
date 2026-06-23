"""Karrio UPS connection settings."""

import attr
import karrio.providers.ups.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """UPS connection settings."""

    # Optional so merchants can connect with only account number + country code
    # when ops has configured a platform-wide UPS app via SYSTEM_CONFIG.
    client_id: str = None  # type:ignore
    client_secret: str = None  # type:ignore
    account_number: str = None

    carrier_id: str = "ups"
    account_country_code: str = None
    test_mode: bool = False
    metadata: dict = {}
    config: dict = {}
    id: str = None
