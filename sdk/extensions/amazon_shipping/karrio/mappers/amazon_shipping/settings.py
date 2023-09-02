"""Karrio Amazon Shipping connection settings."""

import attr
from karrio.providers.amazon_shipping.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Amazon Shipping connection settings."""

    seller_id: str  # type:ignore
    developer_id: str  # type:ignore
    mws_auth_token: str  # type:ignore
    x_amz_access_token: str  # This is the access token retrieved from oauth flow.
    aws_region: str = "us-east-1"

    id: str = None
    test_mode: bool = False
    carrier_id: str = "amazon_shipping"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
