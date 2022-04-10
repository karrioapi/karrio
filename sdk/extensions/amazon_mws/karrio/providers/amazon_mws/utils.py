from karrio.core import Settings as BaseSettings


class Settings(BaseSettings):
    """AmazonMws connection settings."""

    account_country_code: str = None

    @property
    def server_url(self):
        return "https://api.amazon_mws.com/v2"

    @property
    def carrier_name(self):
        return "amazon_mws"
