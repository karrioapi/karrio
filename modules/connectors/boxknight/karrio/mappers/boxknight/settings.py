"""Karrio BoxKnight client settings."""

import attr
import jstruct
import karrio.lib as lib
import karrio.providers.boxknight.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """BoxKnight connection settings."""

    # required carrier specific properties
    username: str
    password: str

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "boxknight"
    account_country_code: str = "CA"
    metadata: dict = {}
    config: dict = {}
