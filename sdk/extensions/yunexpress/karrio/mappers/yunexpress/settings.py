"""Karrio Yunexpress  settings."""

import attr
from karrio.providers.yunexpress.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Yunexpress  connection settings."""

    # Carrier specific properties
    customer_number: str
    api_secret: str

    # Base properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "yunexpress"
    account_country_code: str = None
    metadata: dict = {}
