"""Purplship BoxKnight client settings."""

import attr
from purplship.providers.boxknight.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """BoxKnight connection settings."""

    username: str
    password: str

    id: str = None
    test: bool = False
    carrier_id: str = "boxknight"
    account_country_code: str = "CA"
