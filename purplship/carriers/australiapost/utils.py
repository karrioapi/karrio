"""PurplShip Australia post client settings."""

from base64 import b64encode
from purplship.core.settings import Settings as BaseSettings


class Settings(BaseSettings):
    """Australia post connection settings."""

    api_key: str
    password: str
    account_number: str

    @property
    def server_url(self):
        return (
            "https://digitalapi.auspost.com.au"
            if self.test else
            "https://digitalapi.auspost.com.au"
        )

    @property
    def carrier(self):
        return 'australiapost'

    @property
    def authorization(self):
        return (
            b64encode(f"{self.api_key}:{self.password}".encode("utf-8")).decode("ascii")
            if self.password
            else None
        )
