"""Karrio DPD Group connection settings."""

import typing
import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """DPD Group connection settings."""

    api_key: str
    account_number: str = None

    @property
    def carrier_name(self):
        return "dpd_group"

    @property
    def server_url(self):
        return (
            "https://nst-preprod.dpsin.dpdgroup.com/api/v1.1"
            if self.test_mode
            else "https://shipping.dpdgroup.com/api/v1.1"
        )

    @property
    def tracking_url(self):
        return "https://tracking.dpdgroup.com/track/{}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.dpd_group.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )
