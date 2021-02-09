from purplship.core import Settings as BaseSettings


class Settings(BaseSettings):
    """Sendle connection settings."""

    # username: str
    # password: str
    # account_number: str = None
    id: str = None

    @property
    def carrier_name(self):
        return "sendle"

    @property
    def server_url(self):
        return (
            "https://ct.soa-gw.canadapost.ca"
            if self.test
            else "https://soa-gw.canadapost.ca"
        )
