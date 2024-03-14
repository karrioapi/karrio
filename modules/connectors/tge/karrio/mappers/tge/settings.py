"""Karrio TGE client settings."""

import attr
import karrio.providers.tge.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """TGE connection settings."""

    # required carrier specific properties
    username: str
    password: str
    api_key: str
    toll_username: str
    toll_password: str
    my_toll_token: str
    my_toll_identity: str
    account_code: str = None
    sssc_count: int = 0
    shipment_count: int = 0

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "tge"
    account_country_code: str = "AU"
    metadata: dict = {}
    config: dict = {}
