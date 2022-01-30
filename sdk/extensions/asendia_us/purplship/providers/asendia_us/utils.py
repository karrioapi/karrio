from base64 import b64encode
from purplship.core import Settings as BaseSettings


class Settings(BaseSettings):
    """Asendia US connection settings."""

    # Carrier specific properties
    username: str
    password: str
    x_asendia_one_api_key: str
    account_number: str = None

    id: str = None
    account_country_code: str = "US"

    @property
    def carrier_name(self):
        return "asendia_us"

    @property
    def server_url(self):
        return (
            "https://a1apiuat.asendiausa.com"
            if self.test
            else "https://a1api.asendiausa.com"
        )

    @property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return b64encode(pair.encode("utf-8")).decode("ascii")
