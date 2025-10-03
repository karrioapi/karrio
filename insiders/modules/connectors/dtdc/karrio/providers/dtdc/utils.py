import base64
import datetime
import urllib.parse

import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """DTDC connection settings."""

    # DTDC specific API connection properties
    api_key: str  # API key for authentication
    customer_code: str  # Customer code for DTDC account
    username: str = None  # Username for token authentication
    password: str = None  # Password for token authentication

    @property
    def carrier_name(self):
        return "dtdc"

    @property
    def server_url(self):
        # DTDC API endpoints
        return (
            "https://alphademodashboardapi.shipsy.io"  # sandbox
            if self.test_mode
            else "https://dtdcapi.shipsy.io"  # production
        )

    @property
    def tracking_server_url(self):
        # DTDC tracking API endpoints
        return (
            "http://dtdcstagingapi.dtdc.com/dtdc-tracking-api"  # Staging
            if self.test_mode
            else "https://blktracksvc.dtdc.com"  # Production
        )

    @property
    def label_server_url(self):
        # DTDC label API endpoints
        return (
            "https://alphademodashboardapi.shipsy.io"  # Staging
            if self.test_mode
            else "https://pxapi.dtdc.in"  # Production
        )

    @property
    def tracking_url(self):
        # Public tracking URL for customers
        return "https://www.dtdc.com/tracking?trackid={}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.dtdc.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def access_token(self):
        """Retrieve the access_token for DTDC tracking API using username/password
        or collect it from the cache if an unexpired access_token exists.
        """
        # Only needed for tracking API
        if not self.username or not self.password:
            return None

        cache_key = f"{self.carrier_name}|{self.carrier_id}|{self.api_key}"
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
    """Authenticate with DTDC to get access token for tracking API."""

    response = lib.request(
        url=lib.identity(
            f"{settings.tracking_server_url}/dtdc-api/api/dtdc/authenticate?"
            + urllib.parse.urlencode(
                dict(
                    username=settings.username,
                    password=settings.password,
                )
            )
        ),
        method="GET",
        trace=settings.trace_as("json"),
        on_error=lib.parse_http_response,
        decoder=lambda token: dict(token=token),
    )

    if response.get("error"):
        raise errors.ParsedMessagesError(
            [
                errors.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=response.get("code"),
                    message=response.get("error"),
                )
            ]
        )

    expiry = datetime.datetime.now() + datetime.timedelta(hours=24)

    return {"access_token": response.get("token"), "expiry": lib.fdatetime(expiry)}
