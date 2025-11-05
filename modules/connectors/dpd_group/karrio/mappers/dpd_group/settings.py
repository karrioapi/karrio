"""Karrio DPD Group client settings."""

import attr
import karrio.providers.dpd_group.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """DPD Group connection settings."""

    api_key: str
    account_number: str = None

    # generic properties (DO NOT MODIFY)
    id: str = None
    test_mode: bool = False
    carrier_id: str = "dpd_group"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
