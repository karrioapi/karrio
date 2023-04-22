"""Karrio La Poste client settings."""

import attr
import karrio.providers.laposte.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """La Poste connection settings."""

    # required carrier specific properties
    api_key: str
    lang: str = "fr_FR"

    # generic properties
    id: str = ""
    test_mode: bool = False
    carrier_id: str = "laposte"
    account_country_code: str = "FR"
    metadata: dict = {}
    config: dict = {}
