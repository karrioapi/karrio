import base64
import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """DHL Express connection settings."""

    api_key: str
    api_secret: str

    @property
    def carrier_name(self):
        return "dhl_express"

    @property
    def server_url(self):
        return (
            "https://express.api.dhl.com/mydhlapi/test"
            if self.test_mode
            else "https://express.api.dhl.com/mydhlapi"
        )

    @property
    def tracking_url(self):
        country = self.account_country_code or "US"
        language = self.connection_config.language or "en"
        locale = f"{country}-{language}".lower()
        return (
            "https://www.dhl.com/"
            + locale
            + "/home/tracking/tracking-parcel.html?submit=1&tracking-id={}"
        )

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.dhl_express.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def authorization(self):
        pair = "%s:%s" % (self.api_key, self.api_secret)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")
