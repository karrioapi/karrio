import dpd_lib.Authentication20 as dpd
import karrio.core as core


class Settings(core.Settings):
    """DPD connection settings."""

    delis_id: str
    password: str
    message_language: str = "en_EN"

    @property
    def carrier_name(self):
        return "dpd"

    @property
    def server_url(self):
        return (
            "https://shipperadmintest.dpd.be/PublicApi"
            if self.test_mode
            else "https://wsshipper.dpd.be/soap"
        )

    @property
    def authentication(self):
        return dpd.authentication(
            delisId=self.delis_id,
            authToken=self.auth_token,
            messageLanguage=self.message_language,
        )

    @property
    def auth_token(self):
        """Retrieve the auth token using the delis_id|passwword pair
        or collect it from the cache if an unexpired token exist.
        """
        return "****"

    def login(self):
        pass
