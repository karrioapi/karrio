"""Karrio Nationex client proxy."""

import typing
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.nationex.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/Customers/{self.settings.customer_id}/rates",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={"Authorization": f"Basic {self.settings.authorization}"},
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        payload = request.serialize()
        response = lib.request(
            url=f"{self.settings.server_url}/Shipments",
            data=payload["shipment"],
            trace=self.trace_as("json"),
            method="POST",
            headers={"Authorization": f"Basic {self.settings.authorization}"},
        )

        return lib.Deserializable(
            response,
            lib.to_dict,
            dict(label=payload["label"]),
        )

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/Shipments/{request.serialize()['shipment_id']}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={"Authorization": f"Basic {self.settings.authorization}"},
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, requests: lib.Serializable) -> lib.Deserializable:
        track = lambda shipment_id: (
            shipment_id,
            lib.request(
                url=f"{self.settings.server_url}/Shipments/{shipment_id}?tracking=true",
                trace=self.trace_as("json"),
                method="GET",
                headers={"Authorization": f"Basic {self.settings.authorization}"},
            ),
        )

        responses: typing.List[typing.Tuple[str, str]] = lib.run_asynchronously(
            track, requests.serialize()
        )

        return lib.Deserializable(
            responses,
            lambda response: [(key, lib.to_dict(res)) for key, res in response],
        )
