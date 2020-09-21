"""Purplship Canada post client settings."""

from base64 import b64encode
from purplship.core.settings import Settings as BaseSettings


class Settings(BaseSettings):
    """Canada post connection settings."""

    username: str
    password: str
    customer_number: str
    contract_id: str = None
    language: str = "en"
    id: str = None

    @property
    def carrier_name(self):
        return "canadapost"

    @property
    def server_url(self):
        return (
            "https://ct.soa-gw.canadapost.ca"
            if self.test
            else "https://soa-gw.canadapost.ca"
        )

    @property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return b64encode(pair.encode("utf-8")).decode("ascii")
