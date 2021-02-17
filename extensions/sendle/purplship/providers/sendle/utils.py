from base64 import b64encode
from purplship.core import Settings as BaseSettings


class Settings(BaseSettings):
    """Sendle connection settings."""

    # Carrier specific properties
    sendle_id: str
    api_key: str

    id: str = None

    @property
    def carrier_name(self):
        return "sendle"

    @property
    def server_url(self):
        return (
            "https://sandbox.sendle.com"
            if self.test else
            "https://api.sendle.com"
        )

    @property
    def authorization(self):
        pair = "%s:%s" % (self.sendle_id, self.api_key)
        return b64encode(pair.encode("utf-8")).decode("ascii")
