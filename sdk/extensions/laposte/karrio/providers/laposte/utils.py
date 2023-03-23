
import karrio.core as core


class Settings(core.Settings):
    """La Poste connection settings."""

    # username: str  # carrier specific api credential key

    @property
    def carrier_name(self):
        return "laposte"

    @property
    def server_url(self):
        return (
            "https://carrier.api"
            if self.test_mode
            else "https://sandbox.carrier.api"
        )
