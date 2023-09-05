import base64
import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """DPDHL Germany connection settings."""

    username: str
    password: str
    account_number: str = None

    @property
    def carrier_name(self):
        return "dpdhl"

    @property
    def server_url(self):
        return (
            "https://api-sandbox.dhl.com/parcel/de/shipping/v2"
            if self.test_mode
            else "https://api-eu.dhl.com/parcel/de/shipping/v2"
        )

    @property
    def tracking_url(self):
        country = self.account_country_code or "DE"
        language = self.connection_config.language or "en"
        locale = f"{country}-{language}".lower()
        return (
            "https://www.dhl.com/"
            + locale
            + "/home/tracking/tracking-parcel.html?submit=1&tracking-id={}"
        )

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.dpdhl.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def authorization(self):
        pair = "%s:%s" % (self.api_key, self.api_secret)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")
