"""Karrio Sendle client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.sendle.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/api/products",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/api/orders",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        payload = request.serialize()
        response = lib.request(
            url=f"{self.settings.server_url}/api/orders/{payload['id']}",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "Accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.run_asynchronously(
            lambda payload: (
                payload["ref"],
                lib.request(
                    url=f"{self.settings.server_url}/api/tracking/{payload['ref']}",
                    trace=self.trace_as("json"),
                    method="POST",
                    headers={
                        "Accept": "application/json",
                        "Content-type": "application/json",
                        "Authorization": f"Basic {self.settings.authorization}",
                    },
                ),
            ),
            request.serialize(),
        )

        return lib.Deserializable(
            response,
            lambda __: [(no, lib.to_dict(_)) for no, _ in __],
        )
