"""Purplship Canpar client settings."""

from base64 import b64encode
from purplship.core.settings import Settings as BaseSettings


class Settings(BaseSettings):
    """Canpar connection settings."""


    id: str = None

    @property
    def carrier_name(self):
        return "canpar"

    @property
    def server_url(self):
        pass
