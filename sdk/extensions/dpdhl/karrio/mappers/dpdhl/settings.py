"""Karrio DPDHL Germany client settings."""

import attr
import karrio.providers.dpdhl.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """DPDHL Germany connection settings."""

    # required carrier specific properties
    username: str
    password: str
    account_number: str = None

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "dpdhl"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
