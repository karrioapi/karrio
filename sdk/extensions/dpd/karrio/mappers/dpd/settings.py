
"""Karrio DPD client settings."""

import attr
import karrio.providers.dpd.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """DPD connection settings."""

    # required carrier specific properties

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "dpd"
    account_country_code: str = None
    metadata: dict = {}
