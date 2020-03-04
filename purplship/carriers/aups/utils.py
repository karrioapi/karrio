"""PurplShip Australia post client settings."""
from base64 import b64encode

import attr
from purplship.core.settings import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Australia post connection settings."""

    api_key: str
    password: str = None
    account_number: str = None

    @property
    def authorization(self):
        return b64encode(
            f"{self.api_key}:{self.password}".encode("utf-8")
        ).decode("ascii") if self.password else None
