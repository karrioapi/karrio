"""Karrio HayPost client settings."""

import attr
import karrio.providers.hay_post.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """HayPost connection settings."""

    # required carrier specific properties
    username: str
    password: str
    customer_id: str
    customer_type: str

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "hay_post"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
