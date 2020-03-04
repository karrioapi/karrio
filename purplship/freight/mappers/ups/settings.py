"""PurplShip UPS connection settings."""

from purplship.carriers.ups.utils import Settings as BaseSettings


class Settings(BaseSettings):
    """UPS connection settings."""

    carrier_name: str = "UPS Freight"
    server_url: str = "https://onlinetools.ups.com/webservices"
