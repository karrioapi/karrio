"""Karrio eshipper_xml connection settings."""

import attr
from karrio.providers.eshipper_xml.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """eshipper_xml connection settings."""

    username: str
    password: str

    id: str = None
    test_mode: bool = False
    carrier_id: str = "eshipper_xml"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
