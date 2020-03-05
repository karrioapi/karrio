"""PurplShip USPS client settings."""

from purplship.carriers.usps.utils import Settings as BaseSettings


class Settings(BaseSettings):
    """USPS connection settings."""

    carrier_name: str = "USPS"
    server_url: str = "https://secure.shippingapis.com/ShippingAPI.dll"
