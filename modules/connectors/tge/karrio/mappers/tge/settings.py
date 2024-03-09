"""Karrio TGE client settings."""

import attr
import karrio.providers.tge.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """TGE connection settings."""

    # required carrier specific properties
    api_key: str
    my_toll_identity: str = None
    my_toll_token: str = None
    channel: str = None
    call_id: str = None

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "tge"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
