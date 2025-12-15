"""Karrio DPD Group client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.dpd_group.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        return super().get_rates(request)

    def _get_auth_headers(self) -> dict:
        """Build authentication headers for DPD META-API."""
        token_data = self.settings.access_token
        
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token_data.get('access_token')}",
        }

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """
        Create a shipment with DPD META-API.
        POST /shipping/v1/shipment
        """
        # Get label format from request options or default to PDF
        label_format = getattr(request, "label_format", "PDF") or "PDF"

        response = lib.request(
            url=f"{self.settings.server_url}/shipment?LabelPrintFormat={label_format}",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers=self._get_auth_headers(),
        )

        return lib.Deserializable(response, lib.to_dict)

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """
        Schedule a pickup with DPD META-API.
        POST /shipping/v1/pickupscheduling
        """
        response = lib.request(
            url=f"{self.settings.server_url}/pickupscheduling",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers=self._get_auth_headers(),
        )

        return lib.Deserializable(response, lib.to_dict)
