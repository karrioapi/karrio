"""Karrio Chronopost client settings."""

import attr
from karrio.providers.chronopost.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Chronopost connection settings."""

    account_number: str  # type: ignore
    password: str  # type: ignore
    id_emit: str = "CHRFR"  # type: ignore
    language: str = "en_GB"

    id: str = None
    test_mode: bool = False
    carrier_id: str = "chronopost"
    account_country_code: str = "FR"
    metadata: dict = {}
