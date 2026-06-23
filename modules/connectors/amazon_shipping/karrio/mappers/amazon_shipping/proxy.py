"""Karrio Amazon Shipping API proxy."""

import datetime

import karrio.api.proxy as proxy
import karrio.core.errors as errors
import karrio.core.models as models
import karrio.lib as lib
from karrio.mappers.amazon_shipping.settings import Settings


class Proxy(proxy.Proxy):
    """Amazon Shipping SP-API proxy."""

    settings: Settings

    def authenticate(self, _=None) -> lib.Deserializable[str]:
        """LWA OAuth2 refresh-token flow with a cached access token. See SPECS.md."""
        cache_key = f"{self.settings.carrier_name}|{self.settings.client_id}"

        def get_token():
            result = lib.request(
                url=self.settings.token_url,
                trace=self.trace_as("json"),
                method="POST",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=lib.to_query_string(
                    dict(
                        grant_type="refresh_token",
                        refresh_token=self.settings.refresh_token,
                        client_id=self.settings.client_id,
                        client_secret=self.settings.client_secret,
                    )
                ),
                max_retries=2,
            )

            response = lib.to_dict(result)

            if "error" in response:
                raise errors.ParsedMessagesError(
                    messages=[
                        models.Message(
                            carrier_name=self.settings.carrier_name,
                            carrier_id=self.settings.carrier_id,
                            message=response.get("error_description", response["error"]),
                            code=response.get("error"),
                        )
                    ]
                )

            access_token = response.get("access_token")
            if not access_token:
                raise errors.ParsedMessagesError(
                    messages=[
                        models.Message(
                            carrier_name=self.settings.carrier_name,
                            carrier_id=self.settings.carrier_id,
                            message="Authentication failed: No access token received",
                            code="AUTH_ERROR",
                        )
                    ]
                )

            expiry = datetime.datetime.now() + datetime.timedelta(seconds=float(response.get("expires_in", 3600)))

            return {
                **response,
                "expiry": lib.fdatetime(expiry),
                "access_token": access_token,
            }

        token_state = self.settings.connection_cache.thread_safe(
            refresh_func=get_token,
            cache_key=cache_key,
            buffer_minutes=5,
            token_field="access_token",
        )

        # Handle both Token object and direct dict from cache
        state = token_state.get_state() if hasattr(token_state, "get_state") else token_state
        access_token = state.get("access_token") if isinstance(state, dict) else state

        return lib.Deserializable(access_token)

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        """Get shipping rates using the v2 getRates API."""
        response = self._send_request(
            path="/shipping/v2/shipments/rates",
            request=request,
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        """Create shipment using the oneClickShipment API for combined rate + purchase."""
        response = self._send_request(
            path="/shipping/v2/oneClickShipment",
            request=request,
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        """Cancel shipment using the v2 cancelShipment API."""
        shipment_id = request.serialize()
        response = self._send_request(
            path=f"/shipping/v2/shipments/{shipment_id}/cancel",
            request=None,
            method="PUT",
        )

        return lib.Deserializable(
            response if response.strip() else "{}",
            lib.to_dict,
        )

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        """Get tracking information using the v2 getTracking API."""
        access_token = self.authenticate().deserialize()
        tracking_data = request.serialize()

        def track(data: dict) -> tuple[str, str]:
            tracking_id = data.get("tracking_id")
            carrier_id = data.get("carrier_id", "AMZN_US")

            return (
                tracking_id,
                lib.request(
                    url=f"{self.settings.server_url}/shipping/v2/tracking",
                    trace=self.trace_as("json"),
                    method="GET",
                    headers=self._get_headers(access_token),
                    params=dict(
                        trackingId=tracking_id,
                        carrierId=carrier_id,
                    ),
                ),
            )

        responses: list[tuple[str, str]] = lib.run_asynchronously(track, tracking_data)

        return lib.Deserializable(
            responses,
            lambda res: [(key, lib.to_dict(response)) for key, response in res],
        )

    def _send_request(
        self,
        path: str,
        request: lib.Serializable = None,
        method: str = "POST",
    ) -> str:
        """Send request to Amazon Shipping API."""
        access_token = self.authenticate().deserialize()
        data = dict(data=request.serialize()) if request is not None else {}

        return lib.request(
            url=f"{self.settings.server_url}{path}",
            trace=self.trace_as("json"),
            method=method,
            headers=self._get_headers(access_token),
            **data,
        )

    def _get_headers(self, access_token: str) -> dict:
        """Get request headers with authentication and business ID."""
        headers = {
            "Content-Type": "application/json",
            "x-amz-access-token": access_token,
        }

        # Add shipping business ID if configured
        business_id = self.settings.shipping_business_id or self.settings.connection_config.shipping_business_id.state
        if business_id:
            headers["x-amzn-shipping-business-id"] = business_id

        return headers
