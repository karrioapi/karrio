
"""Karrio DPD Belux client settings."""

import attr
import karrio.providers.dpd_belux.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """DPD Belux connection settings."""

    # required carrier specific properties

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "dpd_belux"
    account_country_code: str = None
    metadata: dict = {}
