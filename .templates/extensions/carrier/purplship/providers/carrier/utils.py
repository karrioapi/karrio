from purplship.core import Settings as BaseSettings


class Settings(BaseSettings):
    """[carrier] connection settings."""

    # username: str
    # password: str
    # account_number: str = None
    id: str = None

    @property
    def carrier_name(self):
        return "carrier"

    @property
    def server_url(self):
        return "https://api.carrier.com/"
