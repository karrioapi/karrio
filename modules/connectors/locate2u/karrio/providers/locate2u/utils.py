import base64
import jstruct
import datetime
import urllib.parse
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """Locate2u connection settings."""

    client_id: str = None
    client_secret: str = None

    id: str = None
    test_mode: bool = False
    carrier_id: str = "locate2u"
    account_country_code: str = "AU"
    metadata: dict = {}

    @property
    def carrier_name(self):
        return "locate2u"

    @property
    def server_url(self):
        return "https://api.locate2u.com"

    @property
    def auth_server_url(self):
        return "https://id.locate2u.com"

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
    import karrio.providers.locate2u.error as error

    result = lib.request(
        url=f"{settings.auth_server_url}/connect/token",
        method="POST",
        headers={
            "content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {settings.authorization}",
        },
        data=urllib.parse.urlencode(
            dict(
                scope="locate2u.api",
                grant_type="client_credentials",
            )
        ),
    )

    response = lib.to_dict(result)
    messages = error.parse_error_response(response, settings)

    if any(messages):
        raise errors.ParsedMessagesError(messages)

    expiry = datetime.datetime.now() + datetime.timedelta(
        seconds=float(response.get("expires_in", 0))
    )

    return {**response, "expiry": lib.fdatetime(expiry)}
