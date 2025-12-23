import typing
import base64
import karrio.lib as lib
import karrio.core.units as units
from karrio.core import Settings as BaseSettings


class Settings(BaseSettings):
    """UPS connection settings."""

    client_id: str
    client_secret: str
    account_number: str = None

    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
    id: str = None

    @property
    def carrier_name(self):
        return "ups"

    @property
    def server_url(self):
        return (
            "https://wwwcie.ups.com"
            if self.test_mode
            else "https://onlinetools.ups.com"
        )

    @property
    def default_currency(self) -> typing.Optional[str]:
        if self.account_country_code in SUPPORTED_COUNTRY_CURRENCY:
            return units.CountryCurrency.map(self.account_country_code).value

        return "USD"

    @property
    def tracking_url(self):
        return "https://www.ups.com/track?loc=en_US&requester=QUIC&tracknum={}/trackdetails"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.ups.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def authorization(self):
        pair = "%s:%s" % (self.client_id, self.client_secret)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")


SUPPORTED_COUNTRY_CURRENCY = ["US", "CA", "FR", "FR", "AU"]
