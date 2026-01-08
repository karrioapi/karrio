"""ParcelOne REST API connection utilities and settings."""

import base64
import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """ParcelOne REST API connection settings."""

    # Required credentials
    username: str
    password: str
    mandator_id: str
    consigner_id: str

    # Generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "parcelone"
    account_country_code: str = "DE"
    metadata: dict = {}
    config: dict = {}

    @property
    def carrier_name(self):
        return "parcelone"

    @property
    def server_url(self):
        return (
            "https://sandboxapi.parcel.one/v1"
            if self.test_mode
            else "https://api.parcel.one/v1"
        )

    @property
    def tracking_url(self):
        return (
            "https://sandboxapi.parcel.one/v1/tracklmc"
            if self.test_mode
            else "https://api.parcel.one/v1/tracklmc"
        )

    @property
    def tracking_link(self):
        return "https://tracking.parcel.one/?trackingNumber={}"

    @property
    def authorization(self):
        """HTTP Basic Auth header value."""
        credentials = f"{self.username}:{self.password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.parcelone.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )
