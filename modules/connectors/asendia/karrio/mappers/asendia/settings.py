"""Karrio Asendia client settings."""

import attr
import karrio.providers.asendia.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Asendia connection settings."""

    # Asendia API credentials (required)
    username: str
    password: str

    # Customer ID for API operations
    customer_id: str = None

    # Generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "asendia"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
