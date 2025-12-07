"""Karrio DPD Group client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.dpd_group.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Create a shipment with DPD Group."""
        response = lib.request(
            url=f"{self.settings.server_url}/shipments",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.api_key}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Get rates from DPD Group."""
        response = lib.request(
            url=f"{self.settings.server_url}/rates",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.api_key}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        """Get tracking information from DPD Group."""
        def _get_tracking(tracking_number: str):
            return tracking_number, lib.request(
                url=f"{self.settings.server_url}/tracking/{tracking_number}",
                trace=self.trace_as("json"),
                method="GET",
                headers={
                    "Authorization": f"Bearer {self.settings.api_key}",
                },
            )

        # Use concurrent requests for multiple tracking numbers
        tracking_numbers = request.serialize()
        responses = lib.run_concurently(_get_tracking, tracking_numbers)

        return lib.Deserializable(
            responses,
            lambda res: [
                (num, lib.to_dict(track)) for num, track in res if any(track.strip())
            ],
        )

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Cancel a shipment with DPD Group."""
        shipment_id = request.serialize()
        response = lib.request(
            url=f"{self.settings.server_url}/shipments/{shipment_id}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={"Authorization": f"Bearer {self.settings.api_key}"},
        )

        return lib.Deserializable(response, lib.to_dict)
