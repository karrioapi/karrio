"""Karrio Generic client settings."""

import karrio.lib as lib
from karrio.core.settings import Settings as BaseSettings


class Settings(BaseSettings):
    """Generic connection settings."""

    @property
    def carrier_name(self):
        return "generic"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.generic.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )
