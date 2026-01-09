
import base64
import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors
from karrio.core.utils.caching import ThreadSafeTokenManager


class Settings(core.Settings):
    """Spring connection settings."""

    # Add carrier specific api connection properties here
    api_key: str
    account_number: str = None

    @property
    def carrier_name(self):
        return "spring"

    @property
    def server_url(self):
        return (
            "https://carrier.api"
            if self.test_mode
            else "https://sandbox.carrier.api"
        )

    # """uncomment the following code block to expose a carrier tracking url."""
    # @property
    # def tracking_url(self):
    #     return "https://www.carrier.com/tracking?tracking-id={}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.spring.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )
