"""SmartKargo connection utilities."""

import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """SmartKargo connection settings."""

    # SmartKargo API key (passed as 'code' header)
    api_key: str
    # Shipper account credentials (required for booking - used as primaryId and account)
    account_number: str
    account_id: str

    @property
    def carrier_name(self):
        return "smartkargo"

    @property
    def server_url(self):
        return (
            "https://uatihub.smartkargo.com/ihub-uat-mt-api-function"
            if self.test_mode
            else "https://ihub.smartkargo.com/ihub-mt-api-function"
        )

    @property
    def tracking_url(self):
        return "https://www.deliverdirect.com/tracking?ref={}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.smartkargo.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )
