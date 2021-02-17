"""Purplship USPS client settings."""

from purplship.core.settings import Settings as BaseSettings


class Settings(BaseSettings):
    """USPS connection settings."""

    # Carrier specific properties
    username: str
    password: str

    id: str = None

    @property
    def carrier_name(self):
        return "usps"

    @property
    def server_url(self):
        return "https://secure.shippingapis.com/ShippingAPI.dll"
