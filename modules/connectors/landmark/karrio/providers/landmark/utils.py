
import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """Landmark Global connection settings."""

    # Add carrier specific api connection properties here
    username: str
    password: str
    client_id: str
    account_number: str = None
    region: str = "Landmark CMH"

    @property
    def carrier_name(self):
        return "landmark"

    @property
    def server_url(self):
        return "https://api.landmarkglobal.com/v2"

    @property
    def tracking_url(self):
        return "https://track.landmarkglobal.com/?search={}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.landmark.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )
