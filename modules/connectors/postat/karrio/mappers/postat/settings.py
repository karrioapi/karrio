"""Karrio PostAT client settings."""

import attr
import karrio.providers.postat.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """PostAT connection settings."""

    # Required credentials (from Austrian Post onboarding)
    client_id: str
    org_unit_id: str
    org_unit_guid: str

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "postat"
    account_country_code: str = "AT"
    metadata: dict = {}
    config: dict = {}
