import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """Hermes connection settings."""

    # OAuth2 credentials (password flow)
    username: str
    password: str
    client_id: str
    client_secret: str

    @property
    def carrier_name(self):
        return "hermes"

    @property
    def server_url(self):
        return (
            "https://de-api-int.hermesworld.com/services/hsi"
            if self.test_mode
            else "https://de-api.hermesworld.com/services/hsi"
        )

    @property
    def token_url(self):
        return (
            "https://authme-int.myhermes.de/authorization-facade/oauth2/access_token"
            if self.test_mode
            else "https://authme.myhermes.de/authorization-facade/oauth2/access_token"
        )

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.hermes.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def access_token(self):
        """Retrieve the access_token using the username|password pair
        or collect it from the cache if an unexpired access_token exists.
        """
        cache_key = f"{self.carrier_name}|{self.username}|{self.client_id}"

        return self.connection_cache.thread_safe(
            refresh_func=lambda: login(self),
            cache_key=cache_key,
            buffer_minutes=5,
        ).get_state()


def login(settings: Settings):
    """Authenticate with Hermes OAuth2 password flow."""
    import karrio.providers.hermes.error as error
    import karrio.core.models as models

    result = lib.request(
        url=settings.token_url,
        trace=settings.trace_as("json"),
        method="POST",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data=lib.to_query_string({
            "grant_type": "password",
            "username": settings.username,
            "password": settings.password,
            "client_id": settings.client_id,
            "client_secret": settings.client_secret,
        }),
    )
    response = lib.to_dict(result)

    # Handle case where response is not a dict
    if not isinstance(response, dict):
        raise errors.ParsedMessagesError(
            messages=[
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code="AUTH_ERROR",
                    message=f"Authentication failed - unexpected response: {str(response)[:200]}",
                )
            ]
        )

    messages = error.parse_error_response(response, settings)

    if any(messages):
        raise errors.ParsedMessagesError(messages=messages)

    expiry = datetime.datetime.now() + datetime.timedelta(
        seconds=float(response.get("expires_in", 3600))
    )
    return {**response, "expiry": lib.fdatetime(expiry)}


def get_access_token(settings: Settings) -> str:
    """Get access token from settings."""
    token_data = settings.access_token
    return token_data.get("access_token") if isinstance(token_data, dict) else token_data


def prepare_shipment_data(request: lib.Serializable) -> tuple:
    """Prepare shipment request data and multi-piece flag."""
    requests_data = request.serialize()
    is_multi_piece = request.ctx.get("is_multi_piece", False) if request.ctx else False
    requests_data = requests_data if isinstance(requests_data, list) else [requests_data]
    return requests_data, is_multi_piece


def inject_parent_shipment_id(req_data: dict, parent_id: str) -> dict:
    """Inject parentShipmentOrderID for multi-piece packages 2+."""
    if req_data.get("service", {}).get("multipartService"):
        req_data["service"]["multipartService"]["parentShipmentOrderID"] = parent_id
    return req_data


def extract_shipment_order_id(response: dict) -> str:
    """Extract shipmentOrderID from response for multi-piece linking."""
    return response.get("shipmentOrderID")
