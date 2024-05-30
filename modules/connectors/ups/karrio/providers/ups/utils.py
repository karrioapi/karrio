import typing
import base64
import jstruct
import datetime
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.errors as errors
from karrio.core import Settings as BaseSettings


class Settings(BaseSettings):
    """UPS connection settings."""

    client_id: str
    client_secret: str
    account_number: str = None

    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
    id: str = None

    @property
    def carrier_name(self):
        return "ups"

    @property
    def server_url(self):
        return (
            "https://wwwcie.ups.com"
            if self.test_mode
            else "https://onlinetools.ups.com"
        )

    @property
    def default_currency(self) -> typing.Optional[str]:
        if self.account_country_code in SUPPORTED_COUNTRY_CURRENCY:
            return units.CountryCurrency.map(self.account_country_code).value

        return "USD"

    @property
    def tracking_url(self):
        return "https://www.ups.com/track?loc=en_US&requester=QUIC&tracknum={}/trackdetails"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.ups.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def authorization(self):
        pair = "%s:%s" % (self.client_id, self.client_secret)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")

    @property
    def access_token(self):
        """Retrieve the access_token using the client_id|client_secret pair
        or collect it from the cache if an unexpired access_token exist.
        """
        cache_key = f"{self.carrier_name}|{self.client_id}|{self.client_secret}"
        now = datetime.datetime.now() + datetime.timedelta(minutes=30)

        auth = self.connection_cache.get(cache_key) or {}
        token = auth.get("access_token")
        expiry = lib.to_date(auth.get("expiry"), current_format="%Y-%m-%d %H:%M:%S")

        if token is not None and expiry is not None and expiry > now:
            return token

        self.connection_cache.set(cache_key, lambda: login(self))
        new_auth = self.connection_cache.get(cache_key)

        return new_auth["access_token"]


def login(settings: Settings):
    import karrio.providers.ups.error as error

    merchant_id = settings.connection_config.merchant_id.state
    result = lib.request(
        url=f"{settings.server_url}/security/v1/oauth/token",
        data="grant_type=client_credentials",
        method="POST",
        headers={
            "authorization": f"Basic {settings.authorization}",
            "content-Type": "application/x-www-form-urlencoded",
            **({"x-merchant-id": merchant_id} if merchant_id else {}),
        },
    )
    response = lib.to_dict(result)
    messages = error.parse_error_response(response, settings)

    if any(messages):
        raise errors.ParsedMessagesError(messages=messages)

    expiry = datetime.datetime.fromtimestamp(
        float(response.get("issued_at")) / 1000
    ) + datetime.timedelta(seconds=float(response.get("expires_in", 0)))
    return {**response, "expiry": lib.fdatetime(expiry)}


SUPPORTED_COUNTRY_CURRENCY = ["US", "CA", "FR", "FR", "AU"]
