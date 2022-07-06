from base64 import b64encode
from karrio.core import Settings as BaseSettings


class Settings(BaseSettings):
    """TNT connection settings."""

    username: str
    password: str
    account_number: str = None
    account_country_code: str = None
    metadata: dict = {}

    id: str = None

    @property
    def carrier_name(self):
        return "tnt"

    @property
    def server_url(self):
        return "https://express.tnt.com"

    @property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return b64encode(pair.encode("utf-8")).decode("ascii")
