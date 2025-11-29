"""Karrio Google Geocoding client utility module."""

import karrio.core as core


class Settings(core.Settings):
    """Google Geocoding connection settings."""

    api_key: str = None

    @property
    def carrier_name(self):
        return "googlegeocoding"

    @property
    def server_url(self):
        return "https://maps.googleapis.com/maps/api/geocode/json"
