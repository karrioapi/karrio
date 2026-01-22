
import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """Spring connection settings."""

    api_key: str

    @property
    def carrier_name(self):
        return "spring"

    @property
    def server_url(self):
        return (
            "https://mtapi.net/?testMode=1"
            if self.test_mode
            else "https://mtapi.net/"
        )

    @property
    def tracking_url(self):
        return "https://www.mailingtechnology.com/tracking/?tn={}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.spring.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )
