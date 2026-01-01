"""Karrio Hermes client proxy."""

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
        access_token = self.settings.access_token.get("access_token")
        language = self.settings.connection_config.language.state or "DE"

        return {
            "Content-Type": "application/json",
            "Accept": accept,
            "Accept-Language": language,
            "Authorization": f"Bearer {access_token}",
        }

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Create a shipment order with label.

        Endpoint: POST /shipmentorders/labels
        """
        label_type = self.settings.connection_config.label_type.state or "PDF"
        accept_header = LabelType.map(label_type).value or "application/pdf"

        response = lib.request(
            url=f"{self.settings.server_url}/shipmentorders/labels",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers=self._get_headers(accept=accept_header),
        )

        return lib.Deserializable(response, lib.to_dict)

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
