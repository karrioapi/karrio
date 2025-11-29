"""Karrio AddressComplete client utility module."""

import karrio.core as core


class Settings(core.Settings):
    """Canada Post AddressComplete connection settings."""

    api_key: str = None

    @property
    def carrier_name(self):
        return "addresscomplete"

    @property
    def server_url(self):
        return "https://ws1.postescanada-canadapost.ca/AddressComplete/Interactive"
