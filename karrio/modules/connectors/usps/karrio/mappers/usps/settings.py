"""Karrio USPS client settings."""

import attr
import karrio.providers.usps.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """USPS connection settings."""

    # Add carrier specific API connection properties here
    client_id: str
    client_secret: str
    account_number: str = None
    account_type: provider_utils.AccountType = "EPS"  # type: ignore
    manifest_MID: str = None
    CRID: str = None
    MID: str = None

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "usps"
    account_country_code: str = "US"
    metadata: dict = {}
    config: dict = {}
