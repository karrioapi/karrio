from karrio.core import Settings as BaseSettings


class Settings(BaseSettings):
    """EasyPost connection settings."""

    account_country_code: str = None

    @property
    def server_url(self):
        return "https://api.easypost.com/v2"

    @property
    def carrier_name(self):
        return "easypost"
