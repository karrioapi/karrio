"""Purplship Generic client settings."""

from purplship.core.settings import Settings as BaseSettings


class Settings(BaseSettings):
    """Generic connection settings."""

    account_number: str = None
    account_country_code: str = None

    id: str = None

    @property
    def carrier_name(self):
        return "generic"
