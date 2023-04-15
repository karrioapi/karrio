"""Karrio GEODIS client settings."""

import attr
import karrio.providers.geodis.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """GEODIS connection settings."""

    # required carrier specific properties
    api_key: str
    identifier: str
    language: str = "fr"

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "geodis"
    account_country_code: str = "FR"
    metadata: dict = {}
    config: dict = {}
