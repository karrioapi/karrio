import base64
import karrio.core as core


class Settings(core.Settings):
    """Sendle connection settings."""

    sendle_id: str
    sendle_api_key: str

    @property
    def carrier_name(self):
        return "sendle"

    @property
    def server_url(self):
        return (
            "https://sandbox.sendle.com" if self.test_mode else "https://api.sendle.com"
        )

    @property
    def authorization(self):
        pair = "%s:%s" % (self.sendle_id, self.sendle_api_key)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")
