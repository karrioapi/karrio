import base64
import karrio.core as core


class Settings(core.Settings):
    """Nationex connection settings."""

    api_key: str
    customer_id: str
    billing_account: str = None
    language: str = "en"

    @property
    def carrier_name(self):
        return "nationex"

    @property
    def server_url(self):
        return (
            "https://apidev.nationex.com/api/v4"
            if self.test_mode
            else "https://api.nationex.com/api/v4"
        )

    @property
    def tracking_url(self):
        return "https://www.nationex.com/" + self.language + "/search?id={}"

    @property
    def authorization(self):
        pair = "%s:%s" % (self.customer_id, self.api_key)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")
