
import base64
import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors
from karrio.core.utils.caching import ThreadSafeTokenManager


class Settings(core.Settings):
    """Teleship connection settings."""

    # Add carrier specific api connection properties here
    client_id: str
    client_secret: str

    @property
    def carrier_name(self):
        return "teleship"

    @property
    def server_url(self):
        return (
            "https://sandbox.teleship.com"
            if self.test_mode
            else "https://api.teleship.com"
        )

    @property
    def tracking_url(self):
        return "https://track.teleship.com/{}"



    @property
    def connection_config(self) -> lib.units.Options:
        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def access_token(self):
        """Retrieve access token using thread-safe token manager"""
        cache_key = f"{self.carrier_name}|{self.client_id}|{self.client_secret}"

        token_manager = self.connection_cache.thread_safe(
            refresh_func=lambda: login(self),
            cache_key=cache_key,
            buffer_minutes=30,
            token_field="access_token",
            expiry_field="expiry",
            expiry_format="%Y-%m-%d %H:%M:%S",
        )

        return token_manager.get_token()


def login(settings: Settings):
    """Retrieve OAuth access token from Teleship API"""
    import karrio.providers.teleship.error as error

    result = lib.request(
        url=f"{settings.server_url}/oauth/token",
        method="POST",
        headers={"content-Type": "application/x-www-form-urlencoded"},
        data=lib.to_query_string(
            dict(
                grant_type="client_credentials",
                client_id=settings.client_id,
                client_secret=settings.client_secret,
            )
        ),
    )

    response = lib.to_dict(result)
    messages = error.parse_error_response(response, settings)

    if any(messages):
        raise errors.ParsedMessagesError(messages)

    # Normalize Teleship's camelCase response to snake_case for consistency
    normalized_response = {
        "access_token": response.get("accessToken"),
        "expires_in": response.get("expiresIn"),
        "token_type": response.get("tokenType"),
        "expiration_time": response.get("expirationTime"),
    }

    expiry = datetime.datetime.now() + datetime.timedelta(
        seconds=float(normalized_response.get("expires_in", 0))
    )
    return {**normalized_response, "expiry": lib.fdatetime(expiry)}


class ConnectionConfig(lib.Enum):
    """Teleship connection configuration."""

    account_id = lib.OptionEnum("account_id", str)
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    label_format = lib.OptionEnum("label_format", str)
