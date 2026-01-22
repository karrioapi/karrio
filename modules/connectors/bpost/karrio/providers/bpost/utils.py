import base64
import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """Belgian Post connection settings."""

    passphrase: str
    account_id: str

    account_country_code: str = "BE"
    config: dict = {}

    @property
    def carrier_name(self):
        return "bpost"

    @property
    def server_url(self):
        return "https://shm-rest.bpost.cloud/services/shm"

    @property
    def tracking_url(self):
        lang = self.connection_config.lang.state or "EN"
        return "https://track.bpost.cloud/btr/web/#/search?itemCode={}&lang=" + lang

    @property
    def authorization(self):
        pair = "%s:%s" % (self.account_id, self.passphrase)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.bpost.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )
