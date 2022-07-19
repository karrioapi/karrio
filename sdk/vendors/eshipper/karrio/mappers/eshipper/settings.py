"""Karrio eshipper connection settings."""

import attr
from karrio.providers.eshipper.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """eshipper connection settings."""

    username: str
    password: str

    id: str = None
    test_mode: bool = False
    carrier_id: str = "eshipper"
    account_country_code: str = None
    metadata: dict = {}
