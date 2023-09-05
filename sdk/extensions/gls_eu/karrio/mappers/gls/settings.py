"""Karrio GLS client settings."""

import attr
import karrio.providers.gls_eu.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """GLS connection settings."""

    # required carrier specific properties
    username: str
    password: str
    contact_id: str

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "gls_eu"
    account_country_code: str = None
    metadata: dict = {}
