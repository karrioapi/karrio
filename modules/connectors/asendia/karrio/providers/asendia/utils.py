"""Karrio Asendia provider utilities."""

import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """Asendia connection settings."""

    # Asendia API credentials
    username: str
    password: str
    customer_id: str = None

    @property
    def carrier_name(self):
        return "asendia"

    @property
    def server_url(self):
        # Asendia only has one environment
        return "https://www.asendia-sync.com"

    @property
    def tracking_url(self):
        return "https://tracking.asendia.com/tracking/{}"

    @property
    def access_token(self):
        """Retrieve the access_token using the username|password pair
        or collect it from the cache if an unexpired access_token exist.
        """
        cache_key = f"{self.carrier_name}|{self.username}|{self.password}"
        now = datetime.datetime.now() + datetime.timedelta(minutes=30)

        auth = self.connection_cache.get(cache_key) or {}
        token = auth.get("id_token")
        expiry = lib.to_date(auth.get("expiry"), current_format="%Y-%m-%d %H:%M:%S")

        if token is not None and expiry is not None and expiry > now:
            return token

        self.connection_cache.set(cache_key, lambda: login(self))
        new_auth = self.connection_cache.get(cache_key)

        return new_auth["id_token"]

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.asendia.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


def login(settings: Settings) -> dict:
    """Authenticate with Asendia API and retrieve JWT token."""
    import karrio.providers.asendia.error as error

    result = lib.request(
        url=f"{settings.server_url}/api/authenticate",
        method="POST",
        headers={"Content-Type": "application/json"},
        data=lib.to_json(
            dict(
                username=settings.username,
                password=settings.password,
            )
        ),
    )

    response = lib.to_dict(result)
    messages = error.parse_error_response(response, settings)

    if any(messages):
        raise errors.ParsedMessagesError(messages=messages)

    # JWT tokens typically expire in 24 hours, set expiry to 23 hours
    expiry = datetime.datetime.now() + datetime.timedelta(hours=23)

    return {
        "id_token": response.get("id_token"),
        "expiry": lib.fdatetime(expiry),
    }
