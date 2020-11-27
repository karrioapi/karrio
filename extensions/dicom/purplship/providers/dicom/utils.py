"""Purplship Dicom client settings."""

from base64 import b64encode
from purplship.core.settings import Settings as BaseSettings


class Settings(BaseSettings):
    """Dicom connection settings."""

    username: str
    password: str
    billing_account: str = None
    id: str = None

    @property
    def carrier_name(self):
        return "dicom"

    @property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return b64encode(pair.encode("utf-8")).decode("ascii")
