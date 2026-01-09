"""Karrio Spring client settings."""

import attr
import karrio.providers.spring.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Spring connection settings."""

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "spring"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
