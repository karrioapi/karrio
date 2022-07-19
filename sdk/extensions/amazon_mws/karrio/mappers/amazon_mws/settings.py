"""Karrio AmazonMws connection settings."""

import attr
from karrio.providers.amazon_mws.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """AmazonMws connection settings."""

    access_key: str
    secret_key: str
    x_amz_access_token: str  # This is the access token retrieved from oauth flow
    aws_region: str = "us-east-1"

    id: str = None
    test_mode: bool = False
    carrier_id: str = "amazon_mws"
    account_country_code: str = None
    metadata: dict = {}
