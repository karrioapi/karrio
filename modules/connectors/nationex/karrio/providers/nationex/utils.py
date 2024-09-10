import base64
import karrio.lib as lib
import karrio.core as core

LanguageEnum = lib.units.create_enum("LanguageEnum", ["en", "fr"])


class Settings(core.Settings):
    """Nationex connection settings."""

    api_key: str
    customer_id: str
    billing_account: str = None
    language: LanguageEnum = "en"  # type: ignore

    @property
    def carrier_name(self):
        return "nationex"

    @property
    def server_url(self):
        return (
            "https://apidev.nationex.com/api/v4"
            if self.test_mode
            else "https://api.nationex.com/api/v4"
        )

    @property
    def tracking_url(self):
        return "https://www.nationex.com/" + self.language + "/search?id={}"

    @property
    def authorization(self):
        pair = "%s:%s" % (self.customer_id, self.api_key)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")
