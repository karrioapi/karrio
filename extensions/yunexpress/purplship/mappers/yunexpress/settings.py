"""Purplship Yunexpress  settings."""

import attr
from purplship.providers.yunexpress.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Yunexpress  connection settings."""

    # Carrier specific properties
    customer_number: str
    api_secret: str

    # Base properties
    id: str = None
    test: bool = False
    carrier_id: str = "yunexpress"
