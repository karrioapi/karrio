from typing import List, Any
from purplship.core.utils import (
    Serializable,
    Deserializable,
    XP,
    request as http,
)
from purplship.core.utils.helpers import exec_async
from purplship.mappers.dhl_poland.settings import Settings
from purplship.api.proxy import Proxy as BaseProxy


class Proxy(BaseProxy):
    settings: Settings

    def _send_request(self, request: Serializable[Any], soapaction: str) -> str:
        return http(
            url=f"{self.settings.server_url}",
            data=bytearray(request.serialize(), "utf-8"),
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "soapaction": soapaction,
            },
            method="POST",
        )

    def get_tracking(self, requests: Serializable) -> Deserializable:
        responses = exec_async(
            lambda request: dict(
                number=request[0],
                data=self._send_request(
                    Serializable(request[1]),
                    soapaction=f"{self.settings.server_url}#getTrackAndTraceInfo",
                ),
            ),
            requests.serialize().items(),
        )

        return Deserializable(
            responses,
            lambda results: {
                result["number"]: XP.to_xml(result["data"]) for result in results
            },
        )

    def create_shipment(self, request: Serializable) -> Deserializable[str]:
        response = self._send_request(
            request,
            soapaction=f"{self.settings.server_url}#createShipment",
        )

        return Deserializable(response, XP.to_xml)

    def cancel_shipment(self, request: Serializable) -> Deserializable[str]:
        response = self._send_request(
            request,
            soapaction=f"{self.settings.server_url}#deleteShipment",
        )

        return Deserializable(response, XP.to_xml)
