
import base64
import datetime
import logging
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors
from karrio.core.utils.caching import ThreadSafeTokenManager

logger = logging.getLogger(__name__)


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
    """Retrieve OAuth access token from Teleship API with comprehensive error handling"""
    import karrio.providers.teleship.error as error

    logger.info(f"Requesting OAuth token from Teleship API (test_mode={settings.test_mode})")

    try:
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
    except Exception as e:
        logger.error(f"Failed to request OAuth token from Teleship API: {str(e)}")
        raise errors.ShippingSDKError(f"OAuth token request failed: {str(e)}") from e

    response = lib.to_dict(result)
    messages = error.parse_error_response(response, settings)

    if any(messages):
        logger.error(f"OAuth token request returned errors: {messages}")
        raise errors.ParsedMessagesError(messages)

    # Log raw response for debugging
    logger.info(f"Raw OAuth response from Teleship: {response}")

    # Normalize Teleship's camelCase response to snake_case for consistency
    normalized_response = {
        "access_token": response.get("accessToken"),
        "expires_in": response.get("expiresIn"),
        "token_type": response.get("tokenType"),
        "expiration_time": response.get("expirationTime"),
    }

    # Log normalized values
    logger.info(
        f"Normalized OAuth response - "
        f"expiresIn: {normalized_response.get('expires_in')}, "
        f"expirationTime: {normalized_response.get('expiration_time')}"
    )

    # Validate access token presence
    if not normalized_response.get("access_token"):
        logger.error("OAuth response missing access token")
        raise errors.ShippingSDKError(
            "OAuth token response is invalid: missing 'accessToken' field"
        )

    # Calculate expiry with multiple fallbacks for robustness
    # NOTE: Teleship returns expiresIn and expirationTime in MILLISECONDS, not seconds
    expires_in = normalized_response.get("expires_in")
    expiration_time = normalized_response.get("expiration_time")

    if expires_in:
        # Convert milliseconds to seconds and use relative time (preferred)
        expires_in_seconds = float(expires_in) / 1000.0
        expiry = datetime.datetime.now() + datetime.timedelta(seconds=expires_in_seconds)
        logger.info(
            f"Using 'expiresIn' field: OAuth token expires in {expires_in_seconds:.1f} seconds "
            f"({expires_in}ms) at {expiry}"
        )
    elif expiration_time:
        # Parse absolute timestamp as fallback (Unix timestamp in milliseconds)
        logger.warning(
            f"OAuth response missing 'expiresIn', using 'expirationTime' fallback: {expiration_time}"
        )
        try:
            # Convert milliseconds to seconds for Unix timestamp
            expiration_timestamp_seconds = float(expiration_time) / 1000.0
            expiry = datetime.datetime.fromtimestamp(expiration_timestamp_seconds)
            logger.info(f"Parsed absolute expiry time: {expiry} from timestamp {expiration_timestamp_seconds}")
        except (ValueError, AttributeError, OSError) as e:
            # If parsing fails, use safe default
            logger.warning(
                f"Failed to parse 'expirationTime' ({expiration_time}): {str(e)}. "
                f"Using 1-hour default expiry"
            )
            expiry = datetime.datetime.now() + datetime.timedelta(hours=1)
    else:
        # Safe default: 1 hour if both fields are missing
        logger.warning(
            "OAuth response missing both 'expiresIn' and 'expirationTime'. "
            "Using 1-hour default expiry"
        )
        expiry = datetime.datetime.now() + datetime.timedelta(hours=1)

    # Validate that expiry is in the future
    if expiry <= datetime.datetime.now():
        logger.warning(
            f"Calculated token expiry ({expiry}) is in the past. "
            f"Resetting to 1-hour default"
        )
        expiry = datetime.datetime.now() + datetime.timedelta(hours=1)

    logger.info(f"OAuth token retrieved successfully, expires at {expiry}")
    return {**normalized_response, "expiry": lib.fdatetime(expiry)}


class ConnectionConfig(lib.Enum):
    """Teleship connection configuration."""

    account_id = lib.OptionEnum("account_id", str)
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    label_format = lib.OptionEnum("label_format", str)
