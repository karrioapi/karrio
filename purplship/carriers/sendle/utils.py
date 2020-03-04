from base64 import b64encode
from purplship.core.settings import Settings as BaseSettings


class Settings(BaseSettings):
    """Sendle connection settings."""

    sendle_id: str
    api_key: str

    @property
    def authorization(self):
        pair = "%s:%s" % (self.sendle_id, self.api_key)
        return b64encode(pair.encode("utf-8")).decode("ascii")
