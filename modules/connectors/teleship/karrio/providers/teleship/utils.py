
import base64
import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors
from karrio.core.utils.caching import ThreadSafeTokenManager


class Settings(core.Settings):
    """Teleship connection settings."""

    # Add carrier specific api connection properties here
    api_key: str
    account_number: str = None

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

#     """uncomment the following code block to implement the oauth login."""
#     @property
#     def access_token(self):
#         """Retrieve the access_token using the client_id|client_secret pair
#         or collect it from the cache if an unexpired access_token exist.
#         """
#         cache_key = f"{self.carrier_name}|{self.client_id}|{self.client_secret}"
#
#         return self.connection_cache.thread_safe(
#             refresh_func=lambda: login(self),
#             cache_key=cache_key,
#             buffer_minutes=30,
#         ).get_state()

# """uncomment the following code block to implement the oauth login."""
# def login(settings: Settings):
#     import karrio.providers.teleship.error as error

#     result = lib.request(
#         url=f"{settings.server_url}/oauth/token",
#         method="POST",
#         headers={"content-Type": "application/x-www-form-urlencoded"},
#         data=lib.to_query_string(
#             dict(
#                 grant_type="client_credentials",
#                 client_id=settings.client_id,
#                 client_secret=settings.client_secret,
#             )
#         ),
#     )

#     response = lib.to_dict(result)
#     messages = error.parse_error_response(response, settings)

#     if any(messages):
#         raise errors.ParsedMessagesError(messages)

#     expiry = datetime.datetime.now() + datetime.timedelta(
#         seconds=float(response.get("expires_in", 0))
#     )
#     return {**response, "expiry": lib.fdatetime(expiry)}


class ConnectionConfig(lib.Enum):
    """Teleship connection configuration."""

    account_id = lib.OptionEnum("account_id", str)
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    label_format = lib.OptionEnum("label_format", str)
