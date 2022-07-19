from base64 import b64encode
from karrio.core import Settings as BaseSettings


class Settings(BaseSettings):
    """Sendle connection settings."""

    # Carrier specific properties
    sendle_id: str
    api_key: str

    id: str = None
    account_country_code: str = "AU"
    metadata: dict = {}

    @property
    def carrier_name(self):
        return "sendle"

    @property
    def server_url(self):
        return (
            "https://sandbox.sendle.com" if self.test_mode else "https://api.sendle.com"
        )

    @property
    def authorization(self):
        pair = "%s:%s" % (self.sendle_id, self.api_key)
        return b64encode(pair.encode("utf-8")).decode("ascii")
