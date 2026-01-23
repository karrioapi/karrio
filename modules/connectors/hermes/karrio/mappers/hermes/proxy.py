"""Karrio Hermes client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.hermes.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy
import karrio.providers.hermes.utils as provider_utils
from karrio.providers.hermes.units import LabelType


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Create shipment order(s) with label(s). Sequential for multi-piece linking."""
        requests_data, is_multi_piece = provider_utils.prepare_shipment_data(request)
        label_type = self.settings.connection_config.label_type.state or "PDF"
        accept_header = LabelType.map(label_type).value or "application/pdf"

        responses, parent_id = [], None
        for idx, req_data in enumerate(requests_data):
            if is_multi_piece and idx > 0 and parent_id:
                req_data = provider_utils.inject_parent_shipment_id(req_data, parent_id)

            response = lib.request(
                url=f"{self.settings.server_url}/shipmentorders/labels",
                data=lib.to_json(req_data),
                trace=self.trace_as("json"),
                method="POST",
                headers={
                    "Content-Type": "application/json",
                    "Accept": accept_header,
                    "Accept-Language": self.settings.connection_config.language.state or "DE",
                    "Authorization": f"Bearer {provider_utils.get_access_token(self.settings)}",
                },
            )

            response_dict = lib.to_dict(response)
            responses.append(response_dict)
            if idx == 0 and is_multi_piece:
                parent_id = provider_utils.extract_shipment_order_id(response_dict)

        return lib.Deserializable(responses, lambda res: res)

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Create a pickup order. Endpoint: POST /pickuporders"""
        response = lib.request(
            url=f"{self.settings.server_url}/pickuporders",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Accept-Language": self.settings.connection_config.language.state or "DE",
                "Authorization": f"Bearer {provider_utils.get_access_token(self.settings)}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Cancel a pickup order. Endpoint: DELETE /pickuporders/{pickupOrderID}"""
        payload = request.serialize()
        pickup_order_id = payload.get("pickupOrderID")

        response = lib.request(
            url=f"{self.settings.server_url}/pickuporders/{pickup_order_id}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Accept-Language": self.settings.connection_config.language.state or "DE",
                "Authorization": f"Bearer {provider_utils.get_access_token(self.settings)}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Get tracking information. Endpoint: GET /shipmentinfo"""
        tracking_numbers = request.serialize()
        query_params = "&".join([f"shipmentID={num}" for num in tracking_numbers])

        response = lib.request(
            url=f"{self.settings.server_url}/shipmentinfo?{query_params}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Accept-Language": self.settings.connection_config.language.state or "DE",
                "Authorization": f"Bearer {provider_utils.get_access_token(self.settings)}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
