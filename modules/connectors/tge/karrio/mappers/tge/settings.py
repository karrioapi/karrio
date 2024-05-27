"""Karrio TGE client settings."""

import attr
import jstruct
import karrio.lib as lib
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
    sscc_count: int = None
    shipment_count: int = None

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "tge"
    account_country_code: str = "AU"
    metadata: dict = {}
    config: dict = {}
