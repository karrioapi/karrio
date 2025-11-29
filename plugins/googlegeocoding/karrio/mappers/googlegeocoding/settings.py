"""Karrio Google Geocoding client settings."""

import attr
import karrio.providers.googlegeocoding.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Google Geocoding connection settings."""

    # Required API key for authentication (kw_only to allow after optional fields)
    api_key: str = attr.ib(kw_only=True)

    # generic properties
    carrier_id: str = "googlegeocoding"
