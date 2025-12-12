"""Karrio DPD Group client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.dpd_group.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def _get_auth_headers(self) -> dict:
        """Build authentication headers for DPD META-API."""
        headers = {
            "Content-Type": "application/json",
            "X-DPD-BUCODE": self.settings.bucode,
        }

        # Add authentication method 1: Username/Password
        if self.settings.username and self.settings.password:
            headers["X-DPD-LOGIN"] = self.settings.username
            headers["X-DPD-PASSWORD"] = self.settings.password

        # Add authentication method 2: Client credentials
        elif self.settings.client_id and self.settings.client_secret:
            headers["X-DPD-CLIENTID"] = self.settings.client_id
            headers["X-DPD-CLIENTSECRET"] = self.settings.client_secret

        return headers

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """
        Create a shipment with DPD META-API.
        POST /shipping/v1/shipment
        """
        # Get label format from request options or default to PDF
        label_format = getattr(request, "label_format", "PDF") or "PDF"

        response = lib.request(
            url=f"{self.settings.server_url}/shipment",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers=self._get_auth_headers(),
            params={"LabelPrintFormat": label_format},
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
