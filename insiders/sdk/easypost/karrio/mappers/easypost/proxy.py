from typing import List, Tuple
from karrio.core.utils import DP, request as http
from karrio.api.proxy import Proxy as BaseProxy
from karrio.core.utils.helpers import exec_async
from karrio.mappers.easypost.settings import Settings
from karrio.core.utils.serializable import Serializable, Deserializable


class Proxy(BaseProxy):
    settings: Settings

    def get_rates(self, request: Serializable) -> Deserializable[str]:
        response = self._send_request(
            path="/shipments", request=Serializable(request.serialize(), DP.jsonify)
        )

        return Deserializable(response, DP.to_dict)

    def create_shipment(self, request: Serializable) -> Deserializable[str]:
        payload = request.serialize()

        def create(request) -> str:
            response = DP.to_dict(
                self._send_request(
                    path="/shipments", request=Serializable(request, DP.jsonify)
                )
            )

            if "error" in response:
                return response

            # retrieve rate with the selected service.
            rate_id = next(
                (
                    rate["id"]
                    for rate in response.get("rates", [])
                    if rate["service"] == payload["service"]
                ),
                None,
            )
            data = DP.to_dict(
                {
                    "rate": {"id": rate_id},
                    "insurance": payload.get("insurance"),
                }
            )

            if rate_id is None:
                raise Exception("No rate found for the given service.")

            return self._send_request(
                path=f"/shipments/{response['id']}/buy",
                request=Serializable(data, DP.jsonify),
            )

        response = create(payload["data"])
        return Deserializable(response, DP.to_dict)

    def cancel_shipment(self, request: Serializable) -> Deserializable[str]:
        response = self._send_request(path=f"/shipments/{request.serialize()}/refund")

        return Deserializable(response, DP.to_dict)

    def get_tracking(self, requests: Serializable) -> Deserializable[str]:
        track = lambda request: (
            request["tracking_code"],
            self._send_request(
                **(
                    dict(path="/trackers", request=Serializable(request, DP.jsonify))
                    if request.get("tracker_id") is None
                    else dict(path=f"/trackers/{request['tracker_id']}", method="GET")
                )
            ),
        )

        responses: List[Tuple[str, str]] = exec_async(track, requests.serialize())
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
                    "Authorization": f"Basic {self.settings.authorization}",
                },
                **data,
            }
        )
