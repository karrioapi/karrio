import dpd_lib.Authentication20 as auth
import dpd_lib.LoginServiceV21 as dpd
import typing
import jstruct
import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.models as models
import karrio.providers.dpd.units as units


class Settings(core.Settings):
    """DPD connection settings."""

    delis_id: str
    password: str
    message_language: str = "en_EN"
    account_country_code: str = "BE"
    cache: dict = {}

    @property
    def carrier_name(self):
        return "dpd"

    @property
    def server_url(self):
        return (
            "https://shipperadmintest.dpd.be/PublicApi"
            if self.test_mode
            else "https://wsshipper.dpd.be"
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
        now = datetime.datetime.now() + datetime.timedelta(minutes=30)
        cache = self.cache or {}

        auth = cache.get(f"{self.delis_id}|{self.password}") or {}
        token = auth.get("token")
        expiry = lib.to_date(auth.get("expiry"), current_format="%Y-%m-%d %H:%M:%S")

        if token is not None and expiry is not None and expiry > now:
            return token

        new_auth = login(self)
        self.cache = {**cache, f"{self.delis_id}|{self.password}": new_auth}

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
    errors = error.parse_error_response(response, settings)

    if any(errors):
        raise Exception(errors)

    return _extract_login_details(response)


def _extract_login_details(node: lib.Element):
    data: dpd.GetAuthResponseDto = lib.find_element(
        "return",
        node,
        dpd.GetAuthResponseDto,
        first=True,
    )
    return dict(
        token=data.authToken,
        expiry=lib.fdatetime(
            data.authTokenExpires,
            current_format="%Y-%m-%dT%H:%M:%S.%f",
        ),
    )
