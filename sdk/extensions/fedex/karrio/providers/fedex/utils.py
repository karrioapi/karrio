import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """FedEx connection settings."""

    api_key: str
    secret_key: str
    account_number: str

    id: str = None
    metadata: dict = {}
    account_country_code: str = None

    @property
    def server_url(self):
        return (
            "https://apis-sandbox.fedex.com"
            if self.test_mode
            else "https://apis.fedex.com"
        )

    @property
    def tracking_url(self):
        return "https://www.fedex.com/fedextrack/?trknbr={}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.fedex.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )
