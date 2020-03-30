"""PurplShip Canada post client settings."""

from base64 import b64encode
from purplship.core.settings import Settings as BaseSettings


class Settings(BaseSettings):
    """Canada post connection settings."""

    username: str
    password: str
    customer_number: str
    contract_id: str = None
    id: str = None

    @property
    def carrier(self):
        return 'caps'

    @property
    def server_url(self):
        return (
            "https://soa-gw.canadapost.ca"
            if self.test else
            "https://ct.soa-gw.canadapost.ca"
        )

    @property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return b64encode(pair.encode("utf-8")).decode("ascii")
