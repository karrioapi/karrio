import karrio.schemas.dpd.Authentication20 as auth
import karrio.schemas.dpd.LoginServiceV21 as dpd

import jstruct
import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """DPD connection settings."""

    delis_id: str
    password: str
    depot: str = None
    message_language: str = "en_EN"
    account_country_code: str = "BE"

    @property
    def carrier_name(self):
        return "dpd"

    @property
    def server_url(self):
        if self.account_country_code == "NL":
            return (
                "https://shipperadmintest.dpd.nl/PublicApi"
                if self.test_mode
                else "https://wsshipper.dpd.nl"
            )

        return (
            "https://shipperadmintest.dpd.be/PublicApi"
            if self.test_mode
            else "https://wsshipper.dpd.be"
        )

    @property
    def tracking_url(self):
        lang = (self.message_language or "en_EN").split("_")[0]
        country = (self.account_country_code or "BE").lower()
        return (
            "https://www.dpdgroup.com/"
            + country
            + "/mydpd/my-parcels/track?lang="
            + lang
            + "&parcelNumber={}"
        )

    @property
    def authentication(self):
        return auth.authentication(
            delisId=self.delis_id,
            authToken=self.auth_token,
            messageLanguage=self.message_language,
        )

    @property
    def auth_token(self):
        """Retrieve the auth token using the delis_id|passwword pair
        or collect it from the cache if an unexpired token exist.
        """
        cache_key = f"{self.carrier_name}|{self.delis_id}|{self.password}"
        now = datetime.datetime.now() + datetime.timedelta(minutes=30)

        auth = self.connection_cache.get(cache_key) or {}
        token = auth.get("token")
        expiry = lib.to_date(auth.get("expiry"), current_format="%Y-%m-%d %H:%M:%S")

        if token is not None and expiry is not None and expiry > now:
            return token

        self.connection_cache.set(cache_key, lambda: login(self))
        new_auth = self.connection_cache.get(cache_key)

        if any(self.depot or "") is False:
            self.depot = new_auth["depot"]

        return new_auth["token"]


def login(settings: Settings):
    import karrio.providers.dpd.error as error

    result = lib.request(
        url=f"{settings.server_url}/soap/services/LoginService/V2_1",
        data=lib.envelope_serializer(
            lib.Envelope(
                Header=lib.Header(),
                Body=lib.Body(
                    dpd.getAuth(
                        delisId=settings.delis_id,
                        password=settings.password,
                        messageLanguage=settings.message_language,
                    )
                ),
            ),
            namespace=(
                'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
                'xmlns:ns="http://dpd.com/common/service/types/LoginService/2.1"'
            ),
            prefixes=dict(
                Envelope="soapenv",
                getAuth="ns",
                delisId="",
                password="",
                messageLanguage="",
            ),
        ),
        method="POST",
        headers={
            "Content-Type": "text/xml;charset=UTF-8",
            "SOAPAction": "http://dpd.com/common/service/types/LoginService/2.1/getAuth",
        },
    )
    response = lib.to_element(result)
    messages = error.parse_error_response(response, settings)

    if any(messages):
        raise errors.ParsedMessagesError(messages=messages)

    return _extract_login_details(response)


def _extract_login_details(node: lib.Element):
    data: dpd.GetAuthResponseDto = lib.find_element(
        "return",
        node,
        dpd.GetAuthResponseDto,
        first=True,
    )
    return dict(
        depot=data.depot,
        token=data.authToken,
        expiry=lib.fdatetime(
            data.authTokenExpires,
            current_format="%Y-%m-%dT%H:%M:%S.%f",
        ),
    )
