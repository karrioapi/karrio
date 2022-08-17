
"""Karrio UPS Freight client settings."""

import attr
import karrio.providers.ups_freight.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """UPS Freight connection settings."""

    # required carrier specific properties

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "ups_freight"
    account_country_code: str = None
    metadata: dict = {}
