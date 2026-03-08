"""Karrio DHL client settings."""

import attr
from karrio.providers.dhl_express.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """DHL connection settings."""

    site_id: str
    password: str
    # password: str = attr.ib(metadata={"sensitive": True})
    account_number: str = None
    account_country_code: str = None
    software_name: str = None
    metadata: dict = {}
    config: dict = {}

    id: str = None
    test_mode: bool = False
    carrier_id: str = "dhl_express"
