import base64
import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """GLS Group connection settings."""

    # OAuth2 credentials
    client_id: str
    client_secret: str

    @property
    def carrier_name(self):
        return "gls_group"

    @property
    def server_url(self):
        return (
            "https://api-sandbox.gls-group.net"
            if self.test_mode
            else "https://api.gls-group.net"
        )

    @property
    def auth_url(self):
        return f"{self.server_url}/oauth2/v2/token"

    @property
    def access_token(self):
        """Retrieve the access_token using the client_id|client_secret pair
        or collect it from the cache if an unexpired access_token exist.
        """
        # Check if connection_cache is available
        if not hasattr(self, 'connection_cache') or self.connection_cache is None:
            # Directly get a new token without caching
            auth = login(self)
            return auth["access_token"]

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

    @property
    def connection_config(self) -> lib.units.Options:
        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


def login(settings: Settings):
    """OAuth2 login to get access token."""
    import karrio.providers.gls_group.error as error

    # Create Basic Auth header for OAuth2
    credentials = f"{settings.client_id}:{settings.client_secret}"
    basic_auth = base64.b64encode(credentials.encode("utf-8")).decode("ascii")

    result = lib.request(
        url=settings.auth_url,
        method="POST",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {basic_auth}",
        },
        data="grant_type=client_credentials",
    )

    response = lib.to_dict(result)
    messages = error.parse_error_response(response, settings)

    if any(messages):
        raise errors.ParsedMessagesError(messages)

    expiry = datetime.datetime.now() + datetime.timedelta(
        seconds=float(response.get("expires_in", 0))
    )
    return {**response, "expiry": lib.fdatetime(expiry)}


class ConnectionConfig(lib.Enum):
    """GLS Group connection configuration."""

    label_format = lib.OptionEnum("label_format", str)
    printer_language = lib.OptionEnum("printer_language", str)
    template_name = lib.OptionEnum("template_name", str)


def parse_error_response(response):
    """Parse the error response from the GLS API."""
    content = lib.failsafe(lambda: lib.decode(response.read()))

    if any(content or ""):
        return content

    return lib.to_json(
        dict(errors=[dict(code=str(response.code), message=response.reason)])
    )
