import base64
import karrio.core as core


class Settings(core.Settings):
    """DHL Express connection settings."""

    username: str
    password: str
    api_key: str

    @property
    def carrier_name(self):
        return "mydhl"

    @property
    def server_url(self):
        return (
            "https://express.api.dhl.com/mydhlapi/test"
            if self.test_mode
            else "https://express.api.dhl.com/mydhlapi"
        )

    @property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")
