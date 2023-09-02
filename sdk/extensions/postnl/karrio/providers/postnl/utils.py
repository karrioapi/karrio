"""Post NL client settings."""

import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """Post NL connection settings."""

    api_key: str
    customer_number: str = None

    @property
    def carrier_name(self):
        return "postnl"

    @property
    def server_url(self):
        return (
            "https://api-sandbox.postnl.nl"
            if self.test_mode
            else "https://api.postnl.nl"
        )

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.postnl.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )
