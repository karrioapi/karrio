import karrio.schemas.fedex.tracking_document_request as fedex
import gzip
import typing
import datetime
import urllib.parse
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """FedEx connection settings."""

    api_key: str = None
    secret_key: str = None
    account_number: str = None
    track_api_key: str = None
    track_secret_key: str = None

    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
    id: str = None

    @property
    def carrier_name(self):
        return "fedex"

    @property
    def server_url(self):
        return (
            "https://apis-sandbox.fedex.com"
            if self.test_mode
            else "https://apis.fedex.com"
        )

    @property
    def tracking_url(self):
        return "https://www.fedex.com/fedextrack/?trknbr={}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.fedex.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def default_currency(self) -> typing.Optional[str]:
        return lib.units.CountryCurrency.map(self.account_country_code).value

    @property
    def access_token(self):
        """Retrieve the access_token using the api_key|secret_key pair
        or collect it from the cache if an unexpired access_token exist.
        """
        if not all([self.api_key, self.secret_key, self.account_number]):
            raise Exception(
                "The api_key, secret_key and account_number are required for Rate, Ship and Other API requests."
            )

        cache_key = f"{self.carrier_name}|{self.api_key}|{self.secret_key}"
        now = datetime.datetime.now() + datetime.timedelta(minutes=30)

        auth = self.connection_cache.get(cache_key) or {}
        token = auth.get("access_token")
        expiry = lib.to_date(auth.get("expiry"), current_format="%Y-%m-%d %H:%M:%S")

        if token is not None and expiry is not None and expiry > now:
            return token

        self.connection_cache.set(
            cache_key,
            lambda: login(
                self,
                client_id=self.api_key,
                client_secret=self.secret_key,
            ),
        )
        new_auth = self.connection_cache.get(cache_key)

        return new_auth["access_token"]

    @property
    def track_access_token(self):
        """Retrieve the access_token using the track_api_key|track_secret_key pair
        or collect it from the cache if an unexpired access_token exist.
        """
        if not all([self.track_api_key, self.track_secret_key]):
            raise Exception(
                "The track_api_key and track_secret_key are required for Track API requests."
            )

        cache_key = f"{self.carrier_name}|{self.track_api_key}|{self.track_secret_key}"
        now = datetime.datetime.now() + datetime.timedelta(minutes=30)

        auth = self.connection_cache.get(cache_key) or {}
        token = auth.get("access_token")
        expiry = lib.to_date(auth.get("expiry"), current_format="%Y-%m-%d %H:%M:%S")

        if token is not None and expiry is not None and expiry > now:
            return token

        self.connection_cache.set(
            cache_key,
            lambda: login(
                self,
                client_id=self.track_api_key,
                client_secret=self.track_secret_key,
            ),
        )
        new_auth = self.connection_cache.get(cache_key)

        return new_auth["access_token"]


def login(settings: Settings, client_id: str = None, client_secret: str = None):
    import karrio.providers.fedex.error as error

    result = lib.request(
        url=f"{settings.server_url}/oauth/token",
        method="POST",
        headers={
            "content-Type": "application/x-www-form-urlencoded",
        },
        data=urllib.parse.urlencode(
            dict(
                grant_type="client_credentials",
                client_id=client_id,
                client_secret=client_secret,
            )
        ),
    )

    response = lib.to_dict(result)
    messages = error.parse_error_response(response, settings)

    if any(messages):
        raise errors.ParsedMessagesError(messages)

    expiry = datetime.datetime.now() + datetime.timedelta(
        seconds=float(response.get("expires_in", 0))
    )

    return {**response, "expiry": lib.fdatetime(expiry)}


def get_proof_of_delivery(tracking_number: str, settings: Settings):
    import karrio.providers.fedex.error as error

    request = fedex.TrackingDocumentRequestType(
        trackDocumentSpecification=[
            fedex.TrackDocumentSpecificationType(
                trackingNumberInfo=fedex.TrackingNumberInfoType(
                    trackingNumber=tracking_number
                )
            )
        ],
        trackDocumentDetail=fedex.TrackDocumentDetailType(
            documentType="SIGNATURE_PROOF_OF_DELIVERY",
            documentFormat="PNG",
        ),
    )
    response = lib.to_dict(
        lib.request(
            url=f"{settings.server_url}/track/v1/trackingdocuments",
            data=lib.to_json(request),
            method="POST",
            decoder=parse_response,
            on_error=lambda b: parse_response(b.read()),
        )
    )

    messages = error.parse_error_response(response, settings)

    if any(messages):
        return None

    return lib.failsafe(
        lambda: lib.bundle_base64(response["output"]["documents"], format="PNG")
    )


def parse_response(binary_string):
    content = lib.failsafe(lambda: gzip.decompress(binary_string)) or binary_string
    return lib.decode(content)


def state_code(address: lib.units.ComputedAddress) -> str:
    if address.state_code is None:
        return None

    return (
        "PQ"
        if address.state_code.lower() == "qc" and address.country_code == "CA"
        else address.state_code
    )
