"""PurplShip Australia post client settings."""

from purplship.carriers.aups.utils import Settings as BaseSettings


class Settings(BaseSettings):
    """Australia post connection settings."""

    carrier_name: str = "Australia Post Shipping"
    server_url: str = "https://digitalapi.auspost.com.au"
