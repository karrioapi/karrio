"""Purplship Generic client settings."""

from purplship.core.settings import Settings as BaseSettings


class Settings(BaseSettings):
    """Generic connection settings."""

    @property
    def carrier_name(self):
        return "generic"
