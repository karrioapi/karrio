"""Karrio SEKO Logistics client settings."""

import attr
import karrio.providers.seko.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """SEKO Logistics connection settings."""

    # Add carrier specific API connection properties here
    access_key: str
    # access_key: str = attr.ib(metadata={"sensitive": True})

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "seko"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
