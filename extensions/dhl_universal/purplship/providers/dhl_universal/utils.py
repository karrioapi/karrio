from purplship.core import Settings as BaseSettings


class Settings(BaseSettings):
    """DHL Universal connection settings."""

    # Carrier specific properties
    consumer_key: str
    consumer_secret: str

    id: str = None

    @property
    def carrier_name(self):
        return "dhl_universal"

    @property
    def server_url(self):
        return "https://api-eu.dhl.com"
