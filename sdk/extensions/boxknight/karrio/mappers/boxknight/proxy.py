"""Karrio BoxKnight client proxy."""

import typing
import base64
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.boxknight.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/rates",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={"Authorization": self.settings.auth_token},
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        payload = request.serialize()
        result = lib.to_dict(
            lib.request(
                url=f"{self.settings.server_url}/orders",
                data=payload["order"],
                trace=self.trace_as("json"),
                method="POST",
                headers={"Authorization": self.settings.auth_token},
            )
        )

        response = (
            dict(
                order_id=result["id"],
                label_type=payload["label_type"],
                service=payload["order"]["service"],
                label=lib.request(
                    url=f"{self.settings.server_url}/labels/{result['id']}?format={payload['label_type']}",
                    decoder=lambda b: base64.encodebytes(b).decode("utf-8"),
                    headers={"Authorization": self.settings.auth_token},
                    trace=self.trace_as("json"),
                ),
            )
            if result.get("error") is None
            else result
        )

        return lib.Deserializable(response)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/orders/{request.serialize()['order_id']}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={"Authorization": self.settings.auth_token},
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, requests: lib.Serializable) -> lib.Deserializable:
        track = lambda data: (
            data["order_id"],
            lib.request(
                url=f"{self.settings.server_url}/orders/{data['order_id']}",
                trace=self.trace_as("json"),
                method="GET",
                headers={"Authorization": self.settings.auth_token},
            ),
        )

        responses: typing.List[typing.Tuple[str, str]] = lib.run_asynchronously(
            track, requests.serialize()
        )

        return lib.Deserializable(
            responses,
            lambda response: [(key, lib.to_dict(res)) for key, res in response],
        )
