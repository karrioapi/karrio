from base64 import b64encode
from purplship.core import Settings as BaseSettings


class Settings(BaseSettings):
    """Yanwen connection settings."""

    # Carrier specific properties
    customer_number: str
    license_key: str

    id: str = None

    @property
    def carrier_name(self):
        return "yanwen"

    @property
    def server_url(self):
        return ""

    @property
    def authorization(self):
        pair = "%s&%s" % (self.customer_number, self.license_key)
        return b64encode(pair.encode("utf-8")).decode("ascii")
