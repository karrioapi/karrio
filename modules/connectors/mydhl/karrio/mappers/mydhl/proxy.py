"""Karrio MyDHL client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.mydhl.settings as provider_settings

# IMPLEMENTATION INSTRUCTIONS:
# 1. Import the schema types specific to your carrier API
# 2. Uncomment and adapt the request examples below to work with your carrier API
# 3. Replace the stub responses with actual API calls once you've tested with the example data
# 4. Update URLs, headers, and authentication methods as required by your carrier API


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/rates",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        payload = request.serialize()
        is_paperless = request.ctx.get("is_paperless", False)

        # Create shipment
        shipment_response = lib.request(
            url=f"{self.settings.server_url}/shipments",
            data=lib.to_json(payload["shipment"]),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        # Extract tracking number from response
        shipment_data = lib.to_dict(shipment_response)
        tracking_number = shipment_data.get("shipmentTrackingNumber")

        # Upload paperless trade documents if applicable
        paperless_response = lib.identity(
            lib.request(
                url=f"{self.settings.server_url}/shipments/{tracking_number}/upload-image",
                data=lib.to_json(payload["paperless"]),
                trace=self.trace_as("json"),
                method="PATCH",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Basic {self.settings.authorization}",
                },
                on_ok=lambda response: dict(ok=True),
            )
            if is_paperless and tracking_number and payload.get("paperless")
            else None
        )

        return lib.Deserializable(
            shipment_response,
            lib.to_dict,
            dict(paperless_response=paperless_response),
        )

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        query_string = request.serialize()
        response = lib.request(
            url=f"{self.settings.server_url}/tracking?{query_string}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/pickups",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def modify_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/pickups",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="PATCH",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        pickup_data = request.serialize()
        confirmation_number = (
            pickup_data
            if isinstance(pickup_data, str)
            else pickup_data.get("confirmationNumber", "")
        )

        response = lib.request(
            url=f"{self.settings.server_url}/pickups/{confirmation_number}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def validate_address(self, request: lib.Serializable) -> lib.Deserializable[str]:
        query_params = request.serialize()
        query_string = "&".join(
            f"{key}={value}" for key, value in query_params.items() if value
        )
        response = lib.request(
            url=f"{self.settings.server_url}/address-validate?{query_string}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def upload_document(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Upload paperless trade documents using the upload-image endpoint."""
        payload = request.serialize()
        tracking_number = payload.pop("shipmentTrackingNumber", None)

        if not tracking_number:
            raise Exception("Tracking number is required for document upload")

        response = lib.request(
            url=f"{self.settings.server_url}/shipments/{tracking_number}/upload-image",
            data=lib.to_json(payload),
            trace=self.trace_as("json"),
            method="PATCH",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
            on_ok=lambda response: dict(ok=True),
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)
