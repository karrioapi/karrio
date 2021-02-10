from purplship.core import Settings as BaseSettings


class Settings(BaseSettings):
    """Aramex connection settings."""

    # Carrier specific properties
    username: str
    password: str
    account_pin: str
    account_entity: str
    account_number: str
    account_country_code: str

    id: str = None

    @property
    def carrier_name(self):
        return "aramex"

    @property
    def server_url(self):
        return (
            "http://ws.dev.aramex.net/shippingapi"
            if self.test
            else "http://ws.aramex.net/shippingapi"
        )
