"""PurplShip USPS client settings."""

from purplship.core.settings import Settings as BaseSettings


class Settings(BaseSettings):
    """USPS connection settings."""

    username: str
    password: str
