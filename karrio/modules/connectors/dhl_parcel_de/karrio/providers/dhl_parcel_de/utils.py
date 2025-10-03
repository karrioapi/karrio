import base64
import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """DHL Parcel DE connection settings."""

    username: str
    password: str
    dhl_api_key: str
    customer_number: str = None

    tracking_consumer_key: str = None
    tracking_consumer_secret: str = None
    account_country_code: str = "DE"

    @property
    def carrier_name(self):
        return "dhl_parcel_de"

    @property
    def server_url(self):
        return (
            "https://api-sandbox.dhl.com/parcel/de/shipping"
            if self.test_mode
            else "https://api-eu.dhl.com/parcel/de/shipping"
        )

    @property
    def tracking_server_url(self):
        return "https://api-eu.dhl.com"

    @property
    def tracking_url(self):
        country = self.account_country_code or "DE"
        language = self.connection_config.language.state or "en"
        locale = f"{country}-{language}".lower()
        return (
            "https://www.dhl.com/"
            + locale
            + "/home/tracking/tracking-parcel.html?submit=1&tracking-id={}"
        )

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.dhl_parcel_de.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def profile(self):
        return self.connection_config.profile.state or "STANDARD_GRUPPENPROFIL"

    @property
    def language(self):
        country = self.account_country_code or "DE"
        language = self.connection_config.language.state or "en"
        return f"{language.lower()}-{country.upper()}"

    @property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")
