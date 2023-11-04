from base64 import b64encode
import base64
from karrio.core import Settings as BaseSettings
from karrio.core.utils.helpers import request


class Settings(BaseSettings):
    """EasyPost connection settings."""

    api_key: str
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}

    @property
    def carrier_name(self):
        return "easypost"

    @property
    def server_url(self):
        return "https://api.easypost.com/v2"

    @property
    def authorization(self):
        pair = "%s:%s" % (self.api_key, "")
        return b64encode(pair.encode("utf-8")).decode("ascii")


def download_label(file_url: str) -> str:
    return request(
        decoder=lambda b: base64.encodebytes(b).decode("utf-8"),
        url=file_url,
    )
