"""Karrio Amazon Shipping connection settings."""

import attr
import jstruct
import karrio.lib as lib
from karrio.providers.amazon_shipping.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Amazon Shipping connection settings."""

    seller_id: str  # type:ignore
    developer_id: str  # type:ignore
    mws_auth_token: str  # type:ignore
    aws_region: str = "us-east-1"

    carrier_id: str = "amazon_shipping"
    account_country_code: str = None
    test_mode: bool = False
    metadata: dict = {}
    config: dict = {}
    id: str = None
