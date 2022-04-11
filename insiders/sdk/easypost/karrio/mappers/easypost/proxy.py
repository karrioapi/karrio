from typing import List, Tuple
from karrio.core.utils import DP, request as http
from karrio.api.proxy import Proxy as BaseProxy
from karrio.core.utils.helpers import exec_async
from karrio.mappers.easypost.settings import Settings
from karrio.core.utils.serializable import Serializable, Deserializable


class Proxy(BaseProxy):
    settings: Settings

    def get_rates(self, requests: Serializable) -> Deserializable[str]:
        create = lambda request: self._send_request(
            path="/shipments", request=Serializable(request)
        )

        responses: List[str] = exec_async(create, requests.serialize())
        return Deserializable(
            responses,
            lambda res: [
                (index, DP.to_dict(response)) for index, response in enumerate(res)
            ],
        )

    def create_shipment(self, requests: Serializable) -> Deserializable[str]:
        create = lambda request: self._send_request(
            path="/shipments", request=Serializable(request)
        )

        responses: List[str] = exec_async(create, requests.serialize())
        return Deserializable(
            responses,
            lambda res: [
                (index, DP.to_dict(response)) for index, response in enumerate(res)
            ],
        )

    def cancel_shipment(self, request: Serializable) -> Deserializable[str]:
        refund = lambda key: (key, self._send_request(path=f"/shipments/{key}/refund"))

        responses: List[Tuple[str, str]] = exec_async(refund, request.serialize())
        return Deserializable(
            responses,
            lambda res: [(key, DP.to_dict(response)) for key, response in res],
        )

    def get_tracking(self, requests: Serializable) -> Deserializable[str]:
        track = lambda request: (
            request["tracking_code"],
            self._send_request(path="/trackers", request=Serializable(request)),
        )

        responses: List[Tuple[str, str]] = exec_async(track, requests.serialize())
        return Deserializable(
            responses,
            lambda res: [(key, DP.to_dict(response)) for key, response in res],
        )

    def _send_request(
        self, path: str, request: Serializable = None, method: str = "POST"
    ) -> str:
        data: dict = (
            dict(data=bytearray(request.serialize(), "utf-8"))
            if request is not None
            else dict()
        )
        return http(
            **{
                "method": method,
                "url": f"{self.settings.server_url}{path}",
                "headers": {
                    "Content-Type": "application/json",
                    "Authorization": f"Basic {self.settings.authorization}",
                },
                **data,
            }
        )
