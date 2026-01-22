"""Karrio Hermes client proxy."""

import typing
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.hermes.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy
from karrio.providers.hermes.units import LabelType


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        return super().get_rates(request)

    def _get_headers(self, accept: str = "application/json") -> dict:
        """Get common headers for Hermes API requests."""
        token_data = self.settings.access_token
        # Handle case where token_data might not be a dict
        access_token = token_data.get("access_token") if isinstance(token_data, dict) else token_data
        language = self.settings.connection_config.language.state or "DE"

        return {
            "Content-Type": "application/json",
            "Accept": accept,
            "Accept-Language": language,
            "Authorization": f"Bearer {access_token}",
        }

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Create shipment order(s) with label(s).

        Endpoint: POST /shipmentorders/labels

        For multi-piece shipments:
        - First package is created and we get shipmentOrderID
        - Subsequent packages include parentShipmentOrderID from first response
        - All requests are made sequentially (required by Hermes API)
        """
        label_type = self.settings.connection_config.label_type.state or "PDF"
        accept_header = LabelType.map(label_type).value or "application/pdf"

        requests_data = request.serialize()
        is_multi_piece = request.ctx.get("is_multi_piece", False) if request.ctx else False

        # Handle single request (backward compatible)
        if not isinstance(requests_data, list):
            requests_data = [requests_data]

        responses: typing.List[dict] = []
        parent_shipment_order_id: typing.Optional[str] = None

        for idx, req_data in enumerate(requests_data):
            # For multi-piece shipments (packages 2+), inject parentShipmentOrderID
            if is_multi_piece and idx > 0 and parent_shipment_order_id:
                # Inject parentShipmentOrderID into the multipartService
                if req_data.get("service") and req_data["service"].get("multipartService"):
                    req_data["service"]["multipartService"]["parentShipmentOrderID"] = parent_shipment_order_id

            # Make the API call
            response = lib.request(
                url=f"{self.settings.server_url}/shipmentorders/labels",
                data=lib.to_json(req_data),
                trace=self.trace_as("json"),
                method="POST",
                headers=self._get_headers(accept=accept_header),
            )

            # Parse response
            response_dict = lib.to_dict(response)
            responses.append(response_dict)

            # Extract shipmentOrderID from first response for multi-piece linking
            if idx == 0 and is_multi_piece:
                parent_shipment_order_id = response_dict.get("shipmentOrderID")

        # Always return list of responses (consistent with Spring/Asendia pattern)
        return lib.Deserializable(
            responses,
            lambda x: x,  # Already parsed
        )

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Create a pickup order.

        Endpoint: POST /pickuporders
        """
        response = lib.request(
            url=f"{self.settings.server_url}/pickuporders",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers=self._get_headers(),
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Cancel a pickup order.

        Endpoint: DELETE /pickuporders/{pickupOrderID}
        """
        payload = request.serialize()
        pickup_order_id = payload.get("pickupOrderID")

        response = lib.request(
            url=f"{self.settings.server_url}/pickuporders/{pickup_order_id}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers=self._get_headers(),
        )

        return lib.Deserializable(response, lib.to_dict)
