"""Karrio Hermes client settings."""

import attr
import karrio.providers.hermes.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Hermes connection settings."""

    # OAuth2 credentials (password flow)
    username: str  # type:ignore
    password: str  # type:ignore
    client_id: str  # type:ignore
    client_secret: str  # type:ignore

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "hermes"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
