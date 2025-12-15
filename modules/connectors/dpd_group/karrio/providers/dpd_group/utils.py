
import base64
import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors
from karrio.core.utils.caching import ThreadSafeTokenManager


class Settings(core.Settings):
    """DPD Group connection settings."""

    # DPD META-API authentication properties
    # Required
    bucode: str  # Business Unit code (X-DPD-BUCODE)

    # Authentication method 1: Username/Password
    username: str = None  # X-DPD-LOGIN
    password: str = None  # X-DPD-PASSWORD

    # Authentication method 2: Client credentials
    client_id: str = None  # X-DPD-CLIENTID
    client_secret: str = None  # X-DPD-CLIENTSECRET

    # Optional account information
    account_number: str = None
    customer_account_number: str = None

    @property
    def carrier_name(self):
        return "dpd_group"

    @property
    def server_url(self):
        return (
            "https://api-preprod.dpsin.dpdgroup.com:8443/shipping/v1"
            if self.test_mode
            else "https://api.dpdgroup.com/shipping/v1"
        )

    @property
    def tracking_url(self):
        return "https://www.dpdgroup.com/tracking?parcelNumber={}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.dpd_group.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def access_token(self):
        """
        Retrieve the access_token using login credentials or from cache.
        Token is valid for 24 hours.
        """
        cache_key = f"{self.carrier_name}|{self.username}|{self.bucode}"

        return self.connection_cache.thread_safe(
            refresh_func=lambda: login(self),
            cache_key=cache_key,
            buffer_minutes=30,  # Refresh 30 mins before expiry (token valid for 24h)
        ).get_state()


def login(settings: Settings):
    """Login to DPD META-API and get access token."""
    import karrio.providers.dpd_group.error as error

    result = lib.request(
        url=f"{settings.server_url}/login",
        trace=settings.trace_as("json"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-DPD-LOGIN": settings.username,
            "X-DPD-PASSWORD": settings.password,
            "X-DPD-BUCODE": settings.bucode,
        },
    )

    # Extract token from response headers
    token = result.headers.get("X-DPD-TOKEN") or result.headers.get("x-dpd-token")

    if not token:
        # Check if there's an error in the response body
        response = lib.to_dict(result)
        messages = error.parse_error_response(response, settings)
        
        if any(messages):
            raise errors.ParsedMessagesError(messages=messages)
        
        raise errors.ShippingSDKError("Failed to obtain DPD access token from login response")

    # Token is valid for 24 hours
    expiry = datetime.datetime.now() + datetime.timedelta(hours=24)
    
    return {
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": 86400,  # 24 hours in seconds
        "expiry": lib.fdatetime(expiry),
    }
