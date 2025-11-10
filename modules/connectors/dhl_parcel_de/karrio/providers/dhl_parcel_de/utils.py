import base64
import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """DHL Parcel DE connection settings."""

    username: str
    password: str
    client_id: str
    client_secret: str
    customer_number: str = None

    account_country_code: str = "DE"

    @property
    def carrier_name(self):
        return "dhl_parcel_de"

    @property
    def server_url(self):
        return (
            "https://api-sandbox.dhl.com/parcel/de/shipping"
            if self.test_mode
            else "https://api-eu.dhl.com/parcel/de/shipping"
        )

    @property
    def token_server_url(self):
        return (
            "https://api-sandbox.dhl.com/parcel/de/account/auth/ropc/v1"
            if self.test_mode
            else "https://api-eu.dhl.com/parcel/de/account/auth/ropc/v1"
        )

    @property
    def tracking_server_url(self):
        return "https://api-eu.dhl.com"

    @property
    def tracking_url(self):
        country = self.account_country_code or "DE"
        language = self.connection_config.language.state or "en"
        locale = f"{country}-{language}".lower()
        return (
            "https://www.dhl.com/"
            + locale
            + "/home/tracking/tracking-parcel.html?submit=1&tracking-id={}"
        )

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.dhl_parcel_de.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def profile(self):
        return self.connection_config.profile.state or "STANDARD_GRUPPENPROFIL"

    @property
    def language(self):
        country = self.account_country_code or "DE"
        language = self.connection_config.language.state or "en"
        return f"{language.lower()}-{country.upper()}"

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


def login(settings: Settings):
    import karrio.providers.ups.error as error

    result = lib.request(
        url=f"{settings.token_server_url}/token",
        trace=settings.trace_as("json"),
        data=lib.to_query_string(
            dict(
                grant_type="password",
                username=settings.username,
                password=settings.password,
                client_id=settings.client_id,
                client_secret=settings.client_secret,
            )
        ),
        method="POST",
        headers={
            "content-Type": "application/x-www-form-urlencoded",
        },
    )
    response = lib.to_dict(result)
    messages = error.parse_error_response(response, settings)

    if any(messages):
        raise errors.ParsedMessagesError(messages=messages)

    # DHL doesn't provide issued_at, so use current time
    expiry = datetime.datetime.now() + datetime.timedelta(
        seconds=int(response.get("expires_in", 0))
    )
    return {**response, "expiry": lib.fdatetime(expiry)}
