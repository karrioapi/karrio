import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """DPD Group base connection settings."""

    @property
    def carrier_name(self):
        return "dpd_meta"

    @property
    def server_url(self):
        return (
            "https://api-preprod.dpsin.dpdgroup.com:8443/shipping/v1"
            if self.test_mode
            else "https://api.dpdgroup.com/shipping/v1"
        )

    @property
    def tracking_url(self):
        return "https://www.dpdgroup.com/tracking?parcelNumber={}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.dpd_meta.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )
