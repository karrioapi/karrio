"""Karrio SmartKargo client settings."""

import attr
import karrio.providers.smartkargo.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """SmartKargo connection settings."""

    # SmartKargo API key (passed as 'code' header)
    api_key: str
    # Shipper account credentials (required for booking - used as primaryId and account)
    account_number: str
    account_id: str

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "smartkargo"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
