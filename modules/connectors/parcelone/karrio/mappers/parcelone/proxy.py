"""Karrio ParcelOne REST API client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.parcelone.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[dict]:
        """Get shipping rates - not directly supported by ParcelOne API.

        ParcelOne returns charges after shipment creation.
        This method creates a shipment with ReturnCharges=1 to get rates.
        """
        response = lib.request(
            url=f"{self.settings.server_url}/shipment",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": self.settings.authorization,
            },
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[dict]:
        """Create a shipment and get label."""
        response = lib.request(
            url=f"{self.settings.server_url}/shipment",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": self.settings.authorization,
            },
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[dict]:
        """Cancel a shipment."""
        data = request.serialize()
        ref_field = data.get("ref_field", "ShipmentID")
        ref_value = data.get("ref_value")

        response = lib.request(
            url=f"{self.settings.server_url}/shipment/{ref_field}/{ref_value}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "Authorization": self.settings.authorization,
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[list]:
        """Get tracking information for multiple tracking numbers."""
        tracking_requests = request.serialize()

        # Make individual requests for each tracking number
        responses = [
            (
                req["tracking_id"],
                lib.to_dict(
                    lib.request(
                        url=f"{self.settings.tracking_url}/tracking/{req['carrier_id']}/{req['tracking_id']}",
                        trace=self.trace_as("json"),
                        method="GET",
                        headers={
                            "Authorization": self.settings.authorization,
                        },
                    )
                ),
            )
            for req in tracking_requests
        ]

        return lib.Deserializable(responses, lambda x: x)
