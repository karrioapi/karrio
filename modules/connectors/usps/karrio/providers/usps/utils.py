"""USPS connection settings."""

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
        return "usps"

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
        cache_key = f"access|{self.carrier_name}|{self.client_id}|{self.client_secret}"
        now = datetime.datetime.now() + datetime.timedelta(minutes=30)

        auth = self.connection_cache.get(cache_key) or {}
        token = auth.get("access_token")
        expiry = lib.to_date(auth.get("expiry"), current_format="%Y-%m-%d %H:%M:%S")

        if token is not None and expiry is not None and expiry > now:
            return token

        self.connection_cache.set(cache_key, lambda: oauth2_login(self))
        new_auth = self.connection_cache.get(cache_key)

        return new_auth["access_token"]

    @property
    def payment_token(self):
        """Retrieve the paymentAuthorizationToken using the client_id|client_secret pair
        or collect it from the cache if an unexpired paymentAuthorizationToken exist.
        """
        cache_key = f"payment|{self.carrier_name}|{self.client_id}|{self.client_secret}"
        now = datetime.datetime.now() + datetime.timedelta(minutes=45)

        auth = self.connection_cache.get(cache_key) or {}
        token = auth.get("paymentAuthorizationToken")
        expiry = lib.to_date(auth.get("expiry"), current_format="%Y-%m-%d %H:%M:%S")

        if token is not None and expiry is not None and expiry > now:
            return token

        self.connection_cache.set(cache_key, lambda: payment_auth(self))
        new_auth = self.connection_cache.get(cache_key)

        return new_auth["paymentAuthorizationToken"]


def oauth2_login(settings: Settings):
    import karrio.providers.usps.error as error

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
                client_id=settings.client_id,
                client_secret=settings.client_secret,
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


def payment_auth(settings: Settings):
    import karrio.providers.usps.error as error

    result = lib.request(
        url=f"{settings.server_url}/payments/v3/payment-authorization",
        method="POST",
        headers={
            "content-Type": "application/json",
            "Authorization": f"Bearer {settings.access_token}",
        },
        data=lib.to_json(
            {
                "roles": [
                    {
                        "roleName": lib.identity(
                            settings.connection_config.role_name.state or "SHIPPER"
                        ),
                        "CRID": settings.connection_config.customer_registration_id.state,
                        "MID": settings.connection_config.mailer_id.state,
                        "accountNumber": settings.account_number,
                        "accountType": settings.account_type or "EPS",
                        "manifestMID": settings.connection_config.manifest_mid.state,
                        "permitNumber": settings.connection_config.permit_number.state,
                        "permitZIP": settings.connection_config.permit_zip.state,
                    }
                ]
            }
        ),
    )

    response = lib.to_dict(result)
    messages = error.parse_error_response(response, settings)

    if any(messages):
        raise errors.ShippingSDKError(messages)

    expiry = datetime.datetime.now() + datetime.timedelta(minutes=45)

    return {**response, "expiry": lib.fdatetime(expiry)}


class ConnectionConfig(lib.Enum):
    role_name = lib.OptionEnum("role_name")
    mailer_id = lib.OptionEnum("mailer_id")
    permit_zip = lib.OptionEnum("permit_zip")
    permit_number = lib.OptionEnum("permit_number")
    customer_registration_id = lib.OptionEnum("customer_registration_id")
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
