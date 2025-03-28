"""Karrio Chit Chats client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.providers.chitchats.utils as provider_utils
import karrio.mappers.chitchats.settings as provider_settings
from typing import Dict, Any


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[Dict[str, Any]]:
        """Get shipping rates from Chit Chats API."""
        response = lib.request(
            url=f"{provider_utils.get_api_url(self.settings)}/{self.settings.client_id}/shipments",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers=provider_utils.get_headers(self.settings),
            on_error=provider_utils.parse_error_response,
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[Dict[str, Any]]:
        """Create a shipment with Chit Chats API."""
        response = lib.request(
            url=f"{provider_utils.get_api_url(self.settings)}/{self.settings.client_id}/shipments",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers=provider_utils.get_headers(self.settings),
            on_error=provider_utils.parse_error_response,
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def buy_shipment(self, request: lib.Serializable) -> lib.Deserializable[Dict[str, Any]]:
        """Buy postage for a shipment."""
        shipment_id = request.ctx.get("shipment_id")
        
        response = lib.request(
            url=f"{provider_utils.get_api_url(self.settings)}/{self.settings.client_id}/shipments/{shipment_id}/buy",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="PATCH",
            headers=provider_utils.get_headers(self.settings),
            on_error=provider_utils.parse_error_response,
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def get_shipment(self, shipment_id: str) -> lib.Deserializable[Dict[str, Any]]:
        """Get details for a specific shipment."""
        response = lib.request(
            url=f"{provider_utils.get_api_url(self.settings)}/{self.settings.client_id}/shipments/{shipment_id}",
            method="GET",
            trace=self.trace_as("json"),
            headers=provider_utils.get_headers(self.settings),
            on_error=provider_utils.parse_error_response,
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_batch(self, request: lib.Serializable) -> lib.Deserializable[Dict[str, Any]]:
        """Create a batch of shipments."""
        response = lib.request(
            url=f"{provider_utils.get_api_url(self.settings)}/{self.settings.client_id}/batches",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers=provider_utils.get_headers(self.settings),
            on_error=provider_utils.parse_error_response,
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def add_to_batch(self, request: lib.Serializable) -> lib.Deserializable[Dict[str, Any]]:
        """Add shipments to a batch."""
        response = lib.request(
            url=f"{provider_utils.get_api_url(self.settings)}/{self.settings.client_id}/shipments/add_to_batch",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="PATCH",
            headers=provider_utils.get_headers(self.settings),
            on_error=provider_utils.parse_error_response,
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx) 
