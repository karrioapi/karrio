"""Karrio La Poste client settings."""

import attr
import karrio.providers.laposte.utils as utils


@attr.s(auto_attribs=True)
class Settings(utils.Settings):
    """La Poste connection settings."""

    # required carrier specific properties
    api_key: str
    lang: utils.LangEnum = "fr_FR"  # type: ignore

    # generic properties
    id: str = ""
    test_mode: bool = False
    carrier_id: str = "laposte"
    account_country_code: str = "FR"
    metadata: dict = {}
    config: dict = {}
