from karrio.core import Settings as BaseSettings


class Settings(BaseSettings):
    """Royal Mail connection settings."""

    # Carrier specific properties
    client_id: str
    client_secret: str

    id: str = None
    account_country_code: str = "UK"
    metadata: dict = {}

    @property
    def carrier_name(self):
        return "royalmail"

    @property
    def server_url(self):
        return (
            "https://api.royalmail.net"
            if self.test_mode
            else "https://api.royalmail.net"
        )
