"""Karrio GLS Group client settings."""

import attr
import karrio.providers.gls_group.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """GLS Group connection settings."""

    # OAuth2 credentials
    client_id: str
    client_secret: str

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "gls_group"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
