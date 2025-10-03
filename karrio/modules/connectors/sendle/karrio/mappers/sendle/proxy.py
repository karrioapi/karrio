"""Karrio Sendle client proxy."""

import urllib.parse
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.providers.sendle.utils as provider_utils
import karrio.mappers.sendle.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, requests: lib.Serializable) -> lib.Deserializable[str]:
        responses = lib.run_asynchronously(
            lambda payload: lib.request(
                url=f"{self.settings.server_url}/api/products?{urllib.parse.urlencode(payload)}",
                trace=self.trace_as("json"),
                method="GET",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Basic {self.settings.authorization}",
                },
            ),
            requests.serialize(),
        )

        return lib.Deserializable(
            responses,
            lambda __: [lib.to_dict(_) for _ in __],
        )

    def create_shipment(self, requests: lib.Serializable) -> lib.Deserializable[str]:
        orders = lib.run_asynchronously(
            lambda payload: lib.request(
                url=f"{self.settings.server_url}/api/orders",
                trace=self.trace_as("json"),
                data=lib.to_json(payload),
                method="POST",
                headers={
                    "Accept": "application/json",
                    "Content-type": "application/json",
                    "Authorization": f"Basic {self.settings.authorization}",
                },
            ),
            requests.serialize(),
        )

        has_failure = provider_utils.check_for_order_failures(orders)

        responses = lib.run_asynchronously(
            lambda data: (
                data["response"],
                (
                    lib.request(
                        url=data["url"],
                        trace=self.trace_as("json"),
                        method=data["method"],
                        headers={
                            "Accept": "application/json",
                            "Content-type": "application/json",
                            "Authorization": f"Basic {self.settings.authorization}",
                        },
                        decoder=provider_utils.label_decoder,
                    )
                    if not data.get("abort")
                    else {}
                ),
            ),
            [
                provider_utils.shipment_next_call(response, self.settings, has_failure)
                for response in orders
            ],
        )

        return lib.Deserializable(
            responses,
            lambda __: [(lib.to_dict(_), label) for _, label in __],
        )

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        payload = request.serialize()
        response = lib.run_asynchronously(
            lambda payload: (
                payload["id"],
                lib.request(
                    url=f"{self.settings.server_url}/api/orders/{payload['id']}",
                    trace=self.trace_as("json"),
                    method="DELETE",
                    headers={
                        "Accept": "application/json",
                        "Content-type": "application/json",
                        "Authorization": f"Basic {self.settings.authorization}",
                    },
                ),
            ),
            payload,
        )

        return lib.Deserializable(
            response,
            lambda __: [(id, lib.to_dict(_)) for id, _ in __],
        )

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.run_asynchronously(
            lambda payload: (
                payload["ref"],
                lib.request(
                    url=f"{self.settings.server_url}/api/tracking/{payload['ref']}",
                    trace=self.trace_as("json"),
                    method="GET",
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
            lambda __: [(ref, lib.to_dict(_)) for ref, _ in __],
        )
