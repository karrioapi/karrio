import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """USPS connection settings."""

    # Add carrier specific api connection properties here
    client_id: str
    client_secret: str
    account_type: str = None
    account_number: str = None

    @property
    def carrier_name(self):
        return "usps_international"

    @property
    def server_url(self):
        return "https://api.usps.com"

    @property
    def tracking_url(self):
        return "https://tools.usps.com/go/TrackConfirmAction?tLabels={}"

    @property
    def connection_config(self) -> lib.units.Options:
        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

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


def login(settings: Settings, client_id: str = None, client_secret: str = None):
    import karrio.providers.usps_international.error as error

    API_SCOPES = [
        "addresses",
        "international-prices",
        "subscriptions",
        "payments",
        "pickup",
        "tracking",
        "labels",
        "scan-forms",
        "companies",
        "service-delivery-standards",
        "locations",
        "international-labels",
        "prices",
    ]
    result = lib.request(
        url=f"{settings.server_url}/oauth2/v3/token",
        method="POST",
        headers={"content-Type": "application/x-www-form-urlencoded"},
        data=lib.to_query_string(
            dict(
                grant_type="client_credentials",
                client_id=client_id,
                client_secret=client_secret,
                scope=" ".join(API_SCOPES),
            )
        ),
    )

    response = lib.to_dict(result)
    messages = error.parse_error_response(response, settings)

    if any(messages):
        raise errors.ShippingSDKError(messages)

    expiry = datetime.datetime.now() + datetime.timedelta(
        seconds=float(response.get("expires_in", 0))
    )

    return {**response, "expiry": lib.fdatetime(expiry)}


class ConnectionConfig(lib.Enum):
    mailer_id = lib.OptionEnum("mailer_id")
    customer_registration_id = lib.OptionEnum("customer_registration_id")
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
