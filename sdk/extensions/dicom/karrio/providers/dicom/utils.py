"""Karrio Dicom client settings."""

from base64 import b64encode
from karrio.core.settings import Settings as BaseSettings


class Settings(BaseSettings):
    """Dicom connection settings."""

    # Carrier specific properties
    username: str
    password: str
    billing_account: str = None

    id: str = None
    account_country_code: str = None
    metadata: dict = {}

    @property
    def carrier_name(self):
        return "dicom"

    @property
    def server_url(self):
        return (
            "https://sandbox-smart4i.dicom.com"
            if self.test_mode
            else "https://smart4i.dicom.com"
        )

    @property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return b64encode(pair.encode("utf-8")).decode("ascii")
