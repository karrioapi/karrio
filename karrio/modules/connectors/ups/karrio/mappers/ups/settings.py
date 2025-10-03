"""Karrio UPS connection settings."""

import attr
import jstruct
import karrio.lib as lib
import karrio.providers.ups.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """UPS connection settings."""

    client_id: str  # type:ignore
    client_secret: str  # type:ignore
    account_number: str = None

    carrier_id: str = "ups"
    account_country_code: str = None
    test_mode: bool = False
    metadata: dict = {}
    config: dict = {}
    id: str = None
