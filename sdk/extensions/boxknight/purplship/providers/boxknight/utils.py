"""Purplship BoxKnight client settings."""

from base64 import b64encode
from purplship.core.settings import Settings as BaseSettings


class Settings(BaseSettings):
    """BoxKnight connection settings."""

    username: str
    password: str

    id: str = None
    account_country_code: str = "CA"

    @property
    def carrier_name(self):
        return "boxknight"

    @property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return b64encode(pair.encode("utf-8")).decode("ascii")
