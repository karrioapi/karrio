from purplship.core import Settings as BaseSettings


class Settings(BaseSettings):
    """[Carrier Name] connection settings."""

    # username: str
    # password: str
    # account_number: str = None
    id: str = None

    @property
    def carrier_name(self):
        return "[carrier_name]"

    @property
    def server_url(self):
        return (
            "https://dev-api.carrier.com"
            if self.test
            else "https://api.carrier.com"
        )
