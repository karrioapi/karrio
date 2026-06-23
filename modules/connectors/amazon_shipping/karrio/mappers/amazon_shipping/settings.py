"""Karrio Amazon Shipping connection settings."""

import attr
import karrio.providers.amazon_shipping.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Amazon Shipping SP-API connection settings. See SPECS.md."""

    # Required LWA SP-API credentials
    client_id: str
    client_secret: str
    refresh_token: str

    # Optional configuration
    aws_region: str = "us-east-1"
    shipping_business_id: str = None

    # Standard karrio settings
    account_country_code: str = None
    carrier_id: str = "amazon_shipping"
    test_mode: bool = False
    metadata: dict = {}
    config: dict = {}
    id: str = None
