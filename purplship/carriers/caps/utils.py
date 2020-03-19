"""PurplShip Canada post client settings."""

from base64 import b64encode
from purplship.core.settings import Settings as BaseSettings


class Settings(BaseSettings):
    """Canada post connection settings."""

    username: str
    password: str
    account_number: str

    @property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return b64encode(pair.encode("utf-8")).decode("ascii")
