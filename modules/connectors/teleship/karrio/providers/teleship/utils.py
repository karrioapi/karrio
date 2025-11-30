import os
import logging
import karrio.lib as lib
import karrio.core as core

logger = logging.getLogger(__name__)


class Settings(core.Settings):
    """Teleship connection settings."""

    # Add carrier specific api connection properties here
    client_id: str
    client_secret: str

    @property
    def carrier_name(self):
        return "teleship"

    @property
    def server_url(self):
        return os.getenv("TELESHIP_SERVER_URL") or (
            "https://sandbox.teleship.com"
            if self.test_mode
            else "https://api.teleship.com"
        )

    @property
    def tracking_url(self):
        return "https://track.teleship.com/{}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.teleship.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def oauth_client_id(self):
        return (
            self.connection_system_config.get("TELESHIP_OAUTH_CLIENT_ID")
            if self.test_mode
            else self.connection_system_config.get("TELESHIP_SANDBOX_OAUTH_CLIENT_ID")
        )

    @property
    def oauth_client_secret(self):
        return (
            self.connection_system_config.get("TELESHIP_OAUTH_CLIENT_SECRET")
            if self.test_mode
            else self.connection_system_config.get(
                "TELESHIP_SANDBOX_OAUTH_CLIENT_SECRET"
            )
        )
