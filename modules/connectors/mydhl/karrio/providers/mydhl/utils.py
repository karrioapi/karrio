import base64
import karrio.core as core


class Settings(core.Settings):
    """DHL Express connection settings."""

    username: str
    password: str
    api_key: str
    account_number: str = None

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
    def tracking_url(self):
        return "https://www.dhl.com/ca-en/home/tracking/tracking-parcel.html?submit=1&tracking-id={}"

    @property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")
