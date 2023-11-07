import base64
import karrio.lib as lib
import karrio.core.settings as settings


class Settings(settings.Settings):
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
