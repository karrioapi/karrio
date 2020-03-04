"""PurplShip DHL client settings."""

from purplship.carriers.dhl.utils import Settings as BaseSettings


class Settings(BaseSettings):
    """DHL connection settings."""

    carrier_name: str = "DHL Freight"
    server_url: str = "https://xmlpi-ea.dhl.com/XMLShippingServlet"

