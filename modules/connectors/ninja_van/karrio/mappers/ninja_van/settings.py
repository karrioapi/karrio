"""Karrio Ninja Van client settings."""

import attr
import karrio.providers.ninja_van.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Ninja Van connection settings."""

    # required carrier specific properties

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "ninja_van"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
