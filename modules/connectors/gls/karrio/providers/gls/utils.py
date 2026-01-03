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
        return "gls"

    @property
    def server_url(self):
        return (
            "https://api-sandbox.gls-group.net"
            if self.test_mode
            else "https://api.gls-group.net"
        )

    @property
    def shipment_api_url(self):
        """ShipIT Farm API base URL for shipment operations."""
        return f"{self.server_url}/shipit-farm/v1/backend"

    @property
    def tracking_api_url(self):
        """Track and Trace API base URL for tracking operations."""
        return f"{self.server_url}/track-and-trace-v1"

    @property
    def auth_url(self):
        return f"{self.server_url}/oauth2/v2/token"

    @property
    def access_token(self):
        """Retrieve the access_token using the client_id|client_secret pair
        or collect it from the cache if an unexpired access_token exist.
        """
        cache_key = f"{self.carrier_name}|{self.client_id}|{self.client_secret}"

        return self.connection_cache.thread_safe(
            refresh_func=lambda: login(self),
            cache_key=cache_key,
            buffer_minutes=30,
        ).get_state()

    @property
    def connection_config(self) -> lib.units.Options:
        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


def login(settings: Settings):
    """OAuth2 login to get access token."""
    import karrio.providers.gls.error as error

    # Create Basic Auth header for OAuth2
    credentials = f"{settings.client_id}:{settings.client_secret}"
    basic_auth = base64.b64encode(credentials.encode("utf-8")).decode("ascii")

    result = lib.request(
        url=settings.auth_url,
        trace=settings.trace_as("json"),
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
        raise errors.ParsedMessagesError(messages=messages)

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
