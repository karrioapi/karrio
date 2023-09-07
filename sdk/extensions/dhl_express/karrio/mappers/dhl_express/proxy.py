"""Karrio DHL Express client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.dhl_express.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/rates",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "content-type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/shipments",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "content-type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/tracking?{request.serialize()}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "content-type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/pickups",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "content-type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def modify_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        payload = request.serialize()
        response = lib.request(
            url=f"{self.settings.server_url}/pickups/{payload['confirmation_number']}",
            data=payload["data"],
            trace=self.trace_as("json"),
            method="PATCH",
            headers={
                "content-type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/pickups/{request.serialize()}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "content-type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def upload_document(self, request: lib.Serializable) -> lib.Deserializable[str]:
        payload = request.serialize()
        response = lib.request(
            url=f"{self.settings.server_url}/shipments/{payload['tracking_number']}/upload-invoice-data",
            data=payload["data"],
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "content-type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
