"""PurplShip FedEx client settings."""

from purplship.carriers.fedex.utils import Settings as BaseSettings


class Settings(BaseSettings):
    """FedEx connection settings."""

    carrier_name: str = "FedEx Freight"
    server_url: str = "https://ws.fedex.com:443/web-services"
