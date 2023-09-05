import base64
import karrio.core as core


class Settings(core.Settings):
    """Asendia US connection settings."""

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
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")
