"""Karrio Chronopost client settings."""

import attr
from karrio.providers.chronopost import utils


@attr.s(auto_attribs=True)
class Settings(utils.Settings):
    """Chronopost connection settings."""

    account_number: str  # type: ignore
    password: str  # type: ignore
    id_emit: str = "CHRFR"  # type: ignore
    language: utils.LanguageEnum = "en_GB"  # type: ignore

    id: str = None
    test_mode: bool = False
    carrier_id: str = "chronopost"
    account_country_code: str = "FR"
    metadata: dict = {}
    config: dict = {}
