import base64
import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """GLS connection settings."""

    username: str
    password: str
    contact_id: str

    @property
    def carrier_name(self):
        return "gls_eu"

    @property
    def server_url(self):
        return "http://fpcs.gls_eu-group.eu"

    @property
    def tracking_url(self):
        country = self.account_country_code or "CA"
        language = self.connection_config.language or "en"
        locale = f"{country}-{language}".lower()
        return (
            "https://www.dhl.com/"
            + locale
            + "/home/tracking/tracking-parcel.html?submit=1&tracking-id={}"
        )

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.gls_eu.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")
