"""PurplShip Canada post client settings."""

from purplship.carriers.caps import Settings as BaseSettings


class Settings(BaseSettings):
    """Canada post connection settings."""

    carrier_name: str = "CanadaPost"
    server_url: str = "https://soagw.canadapost.ca"
