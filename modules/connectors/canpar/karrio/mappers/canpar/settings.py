"""Karrio Canpar client settings."""

import attr
import karrio.providers.canpar.utils as utils


@attr.s(auto_attribs=True)
class Settings(utils.Settings):
    """Canpar connection settings."""

    username: str
    password: str
    language: utils.LanguageEnum = "en"  # type: ignore

    id: str = None
    test_mode: bool = False
    carrier_id: str = "canpar"
    account_country_code: str = "CA"
    metadata: dict = {}
    config: dict = {}
