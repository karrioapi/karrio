import base64
import urllib.parse
from typing import List, Tuple
from purplship.core.utils import DP, Serializable, Deserializable, request as http, exec_async
from purplship.api.proxy import Proxy as BaseProxy
from purplship.mappers.asendia_us.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    def _request(self, path: str, method: str = "GET", **kwargs):
        return http(
            url=f"{self.settings.server_url}{path}",
            headers={
                "Accept": "application/json",
                "Authorization": f"Basic {self.settings.authorization}"
            },
            method=method,
            **kwargs
        )

    # Proxy Methods

    def get_tracking(self, request: Serializable) -> Deserializable[List[str]]:
        def _get_tracking(ref: str):
            return self._request(
                f"/api/A1/v1.0/Tracking/Milestone?trackingNumberVendor={ref}")

        responses: List[str] = exec_async(_get_tracking, request.serialize())

        return Deserializable(
            responses,
            lambda res: [DP.to_dict(track) for track in res if any(track.strip())]
        )

    def get_rates(self, request: Serializable) -> Deserializable[str]:
        query = urllib.parse.urlencode(request.serialize())
        response = self._request(
            f"/api/A1/v1.0/ShippingPlatform/ShippingRate?{query}")

        return Deserializable(response, DP.to_dict)

    def create_shipment(self, request: Serializable) -> Deserializable[str]:
        response = self._request(
            f"/api/A1/v1.0/ShippingPlatform/Package", "POST",
            data=bytearray(request.serialize(), "utf-8")
        )

        return Deserializable(response, DP.to_dict)

    def cancel_shipment(self, request: Serializable) -> Deserializable[Tuple[str, dict]]:
        data = request.serialize()
        query = urllib.parse.urlencode(data)
        response = self._request(
            f"/api/A1/v1.0/ShippingPlatform/Package?{query}", "DELETE")
        
        def deserialize(response: str) -> Tuple[str, dict]:
            content = DP.to_dict(response)
            labelUrl = next(
                (label['content'] for label in (content.get("packageLabel") or {}).get("labels") or []),
                None
            )

            if labelUrl is not None:
                label = self._request(
                    labelUrl, decoder=lambda b: base64.encodebytes(b).decode("utf-8"))

                return label, content

            return None, content

        return Deserializable(response, deserialize)
