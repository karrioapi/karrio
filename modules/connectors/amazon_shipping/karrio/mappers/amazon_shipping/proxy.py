import typing
import karrio.lib as lib
import karrio.api.proxy as proxy
from karrio.mappers.amazon_shipping.settings import Settings


class Proxy(proxy.Proxy):
    settings: Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request(
            path="/shipping/v1/rates",
            request=lib.Serializable(request, lib.to_json),
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request(
            path="/shipping/v1/purchaseShipment",
            request=lib.Serializable(request, lib.to_json),
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request(
            path=f"/shipping/v1/shipments/{request.serialize()}/cancel",
        )

        return lib.Deserializable(response if any(response) else "{}", lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        track = lambda trackingId: (
            trackingId,
            self._send_request(
                path=f"/shipping/v1/tracking/{trackingId}",
                method="GET",
            ),
        )

        responses: typing.List[typing.Tuple[str, str]] = lib.run_asynchronously(
            track, request.serialize()
        )
        return lib.Deserializable(
            responses,
            lambda res: [(key, lib.to_dict(response)) for key, response in res],
        )

    def _send_request(
        self, path: str, request: lib.Serializable = None, method: str = "POST"
    ) -> str:
        data: dict = dict(data=request.serialize()) if request is not None else dict()
        return lib.request(
            **{
                "url": f"{self.settings.server_url}{path}",
                "trace": self.trace_as("json"),
                "method": method,
                "headers": {
                    "Content-Type": "application/json",
                    "x-amz-access-token": self.settings.access_token,
                },
                **data,
            }
        )
