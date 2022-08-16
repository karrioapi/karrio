from typing import Any
from karrio.core.utils import (
    Serializable,
    Deserializable,
    request as http,
    XP,
)
from karrio.mappers.chronopost.settings import Settings
from karrio.api.proxy import Proxy as BaseProxy


class Proxy(BaseProxy):
    settings: Settings

    def _send_request(self, request: Serializable[Any]) -> str:
        return http(
            url=f"{self.settings.server_url}",
            data=bytearray(request.serialize(), "utf-8"),
            headers={
                "Content-Type": "text/xml; charset=utf-8",
            },
            method="POST",
        )

    def get_rates(self, request: Serializable) -> Deserializable:
        response = self._send_request(
            request,
        )
        return Deserializable(response, XP.to_xml)

    def create_shipment(self, request: Serializable) -> Deserializable[str]:
        response = self._send_request(
            request,
        )

        return Deserializable(response, XP.to_xml)

    def cancel_shipment(self, request: Serializable) -> Deserializable[str]:
        response = self._send_request(
            request,
        )

        return Deserializable(response, XP.to_xml)
