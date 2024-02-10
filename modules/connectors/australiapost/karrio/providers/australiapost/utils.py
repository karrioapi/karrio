import base64
import karrio.core as core


class Settings(core.Settings):
    """Australia Post connection settings."""

    # Carrier specific properties
    api_key: str
    password: str
    account_number: str

    account_country_code: str = "AU"

    @property
    def carrier_name(self):
        return "australiapost"

    @property
    def server_url(self):
        return (
            "https://digitalapi.auspost.com.au/test"
            if self.test_mode
            else "https://digitalapi.auspost.com.au"
        )

    @property
    def tracking_url(self):
        return "https://auspost.com.au/mypost/beta/track/details/{}"

    @property
    def authorization(self):
        pair = "%s:%s" % (self.api_key, self.password)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")
