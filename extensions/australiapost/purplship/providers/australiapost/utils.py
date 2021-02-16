from base64 import b64encode
from purplship.core import Settings as BaseSettings


class Settings(BaseSettings):
    """Australia Post connection settings."""

    # Carrier specific properties
    api_key: str
    password: str
    account_number: str

    id: str = None

    @property
    def carrier_name(self):
        return "australiapost"

    @property
    def server_url(self):
        return (
            "https://digitalapi.auspost.com.au/test"
            if self.test else
            "https://digitalapi.auspost.com.au"
        )

    @property
    def authorization(self):
        return (
            b64encode(f"{self.api_key}:{self.password}".encode("utf-8")).decode("ascii")
            if self.password
            else None
        )
