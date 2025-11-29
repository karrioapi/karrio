"""Karrio AddressComplete client settings."""

import attr
import karrio.providers.addresscomplete.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Canada Post AddressComplete connection settings."""

    # Required API key for authentication (kw_only to allow after optional fields)
    api_key: str = attr.ib(kw_only=True)

    # generic properties
    carrier_id: str = "addresscomplete"
