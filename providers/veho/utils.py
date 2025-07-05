from karrio.core import Settings as BaseSettings
import karrio.lib as lib


class Settings(BaseSettings):
    """Veho connection settings."""

    @property
    def carrier_name(self):
        return "veho"

    @property
    def server_url(self):
        return (
            "https://api.sandbox.shipveho.com/v2"
            if self.test_mode
            else "https://api.shipveho.com/v2"
        )

    @property
    def tracking_url(self):
        # Veho tracking via package ID or barcode
        return "https://track.shipveho.com/tracking/{}"

    @property
    def connection_config(self):
        return lib.to_dict(
            {
                # Veho uses 'apikey' header for authentication
                "apikey": self.password,
                "Content-Type": "application/json",
            }
        ) 
