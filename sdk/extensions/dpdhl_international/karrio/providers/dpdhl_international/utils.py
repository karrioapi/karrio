import base64
import jstruct
import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """Deutsche Post International connection settings."""

    consumer_key: str
    consumenr_secret: str
    account_number: str = None

    account_country_code: str = "DE"
    cache: lib.Cache = jstruct.JStruct[lib.Cache]

    @property
    def carrier_name(self):
        return "dpdhl_international"

    @property
    def server_url(self):
        return (
            "https://api-sandbox.dhl.com" if self.test_mode else "https://api.dhl.com"
        )

    @property
    def tracking_url(self):
        country = self.account_country_code or "DE"
        language = self.connection_config.language or "en"
        locale = f"{country}-{language}".lower()
        return (
            "https://www.dhl.com/"
            + locale
            + "/home/tracking/tracking-parcel.html?submit=1&tracking-id={}"
        )

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.dpdhl_international.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def authorization(self):
        pair = "%s:%s" % (self.consumer_key, self.consumenr_secret)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")

    @property
    def access_token(self):
        """Retrieve the access_token using the client_id|client_secret pair
        or collect it from the cache if an unexpired access_token exist.
        """
        cache_key = f"{self.carrier_name}|{self.consumer_key}|{self.consumenr_secret}"
        now = datetime.datetime.now() + datetime.timedelta(minutes=30)

        auth = self.cache.get(cache_key) or {}
        token = auth.get("access_token")
        expiry = lib.to_date(auth.get("expiry"), current_format="%Y-%m-%d %H:%M:%S")

        if token is not None and expiry is not None and expiry > now:
            return token

        self.cache.set(cache_key, lambda: login(self))
        new_auth = self.cache.get(cache_key)

        return new_auth["access_token"]


def login(settings: Settings):
    import karrio.providers.dpdhl_international.error as error

    result = lib.request(
        url=f"{settings.server_url}/security/v1/oauth/token",
        data="grant_type=client_credentials",
        method="POST",
        headers={
            "authorization": f"Basic {settings.authorization}",
            "content-Type": "application/x-www-form-urlencoded",
        },
    )
    response = lib.to_dict(result)
    messages = error.parse_error_response(response, settings)

    if any(messages):
        raise errors.ParsedMessagesError(messages=messages)

    return {
        **response,
        "expiry": lib.fdatetime(
            float(response.get("expires_in", 0)),
            current_format="%Y-%m-%dT%H:%M:%S.%f",
        ),
    }
