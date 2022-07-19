from typing import List, Tuple
from karrio.core.utils import DP, request as http
from karrio.api.proxy import Proxy as BaseProxy
from karrio.core.utils.helpers import exec_async
from karrio.mappers.amazon_mws.settings import Settings
from karrio.core.utils.serializable import Serializable, Deserializable


class Proxy(BaseProxy):
    settings: Settings

    def get_rates(self, request: Serializable) -> Deserializable[str]:
        response = self._send_request(
            path="/shipping/v1/rates",
            request=Serializable(request, DP.jsonify),
        )

        return Deserializable(response, DP.to_dict)

    def create_shipment(self, request: Serializable) -> Deserializable[str]:
        response = self._send_request(
            path="/shipping/v1/purchaseShipment",
            request=Serializable(request, DP.jsonify),
        )

        return Deserializable(response, DP.to_dict)

    def cancel_shipment(self, request: Serializable) -> Deserializable[str]:
        response = self._send_request(
            path=f"/shipping/v1/shipments/{request.serialize()}/cancel",
        )

        return Deserializable(response if any(response) else "{}", DP.to_dict)

    def get_tracking(self, request: Serializable) -> Deserializable[str]:
        track = lambda trackingId: (
            trackingId,
            self._send_request(
                path=f"/shipping/v1/tracking/{trackingId}",
                method="GET",
            ),
        )

        responses: List[Tuple[str, str]] = exec_async(track, request.serialize())
        return Deserializable(
            responses,
            lambda res: [(key, DP.to_dict(response)) for key, response in res],
        )

    def _send_request(
        self, path: str, request: Serializable = None, method: str = "POST"
    ) -> str:
        data: dict = dict(data=request.serialize()) if request is not None else dict()
        return http(
            **{
                "url": f"{self.settings.server_url}{path}",
                "trace": self.trace_as("json"),
                "method": method,
                "headers": {
                    "Content-Type": "application/json",
                    "x-amz-access-token": self.settings.x_amz_access_token,
                },
                **data,
            }
        )
