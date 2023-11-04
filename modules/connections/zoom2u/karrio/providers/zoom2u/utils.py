import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """Zoom2u connection settings."""

    api_key: str

    account_country_code: str = "AU"
    metadata: dict = {}
    config: dict = {}

    @property
    def carrier_name(self):
        return "zoom2u"

    @property
    def server_url(self):
        return "https://api.zoom2u.com"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.zoom2u.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


def clean_response(response: str):
    return response.replace("tracking-link", "trackinglink")
