import jstruct
import datetime
import urllib.parse
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """FedEx connection settings."""

    api_key: str
    secret_key: str
    account_number: str = None

    cache: lib.Cache = jstruct.JStruct[lib.Cache]
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
    id: str = None

    @property
    def carrier_name(self):
        return "fedex"

    @property
    def server_url(self):
        return (
            "https://apis-sandbox.fedex.com"
            if self.test_mode
            else "https://apis.fedex.com"
        )

    @property
    def tracking_url(self):
        return "https://www.fedex.com/fedextrack/?trknbr={}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.fedex.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def access_token(self):
        """Retrieve the access_token using the api_key|secret_key pair
        or collect it from the cache if an unexpired access_token exist.
        """
        cache_key = f"{self.carrier_name}|{self.api_key}|{self.secret_key}"
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
    import karrio.providers.fedex.error as error

    result = lib.request(
        url=f"{settings.server_url}/oauth/token",
        method="POST",
        headers={
            "content-Type": "application/x-www-form-urlencoded",
        },
        data=urllib.parse.urlencode(
            dict(
                grant_type="client_credentials",
                client_id=settings.api_key,
                client_secret=settings.secret_key,
            )
        ),
    )

    response = lib.to_dict(result)
    messages = error.parse_error_response(response, settings)

    if any(messages):
        raise errors.ShippingSDKError(messages)

    expiry = datetime.datetime.now() + datetime.timedelta(
        seconds=float(response.get("expires_in", 0))
    )

    return {**response, "expiry": lib.fdatetime(expiry)}
