
"""Karrio BoxKnight client settings."""

import attr
import karrio.providers.boxknight.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """BoxKnight connection settings."""

    # required carrier specific properties

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "boxknight"
    account_country_code: str = None
    metadata: dict = {}
