import base64
import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """Asendia US connection settings."""

    username: str
    password: str
    api_key: str
    account_number: str = None

    config: dict = {}

    @property
    def carrier_name(self):
        return "asendia_us"

    @property
    def server_url(self):
        return (
            "https://a1apiuat.asendiausa.com"
            if self.test_mode
            else "https://a1api.asendiausa.com"
        )

    @property
    def connection_config(self) -> lib.units.Options:
        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")


class ConnectionConfig(lib.Enum):
    sub_account = lib.OptionEnum("sub_account")
    processing_location = lib.OptionEnum("processing_location")
