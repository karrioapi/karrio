import typing
import dpd_lib.Authentication20 as dpd
import karrio.core as core
import karrio.providers.dpd.units as units


class Settings(core.Settings):
    """DPD connection settings."""

    delis_id: str
    password: str
    message_language: str = "en_EN"
    account_country_code: str = "BE"

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

    def __getattr__(self, __name: str) -> typing.Any:
        _value = super().__getattr__(__name)

        if __name != 'services':
            return _value

        if any(_value or []):
            return _value

        if self.account_country_code == "NL":
            return units.DEFAULT_NL_SERVICES

        return units.DEFAULT_NL_SERVICES


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
