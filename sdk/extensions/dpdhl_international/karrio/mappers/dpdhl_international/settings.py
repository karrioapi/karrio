
"""Karrio Deutsche Post International client settings."""

import attr
import karrio.providers.dpdhl_international.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Deutsche Post International connection settings."""

    # required carrier specific properties

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "dpdhl_international"
    account_country_code: str = None
    metadata: dict = {}
