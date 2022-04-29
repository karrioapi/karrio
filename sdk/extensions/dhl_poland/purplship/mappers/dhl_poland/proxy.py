from typing import Any
from purplship.core.utils import (
    Serializable,
    Deserializable,
    request as http,
    XP,
)
from purplship.universal.mappers.rating_proxy import RatingMixinProxy
from purplship.core.utils.helpers import exec_async
from purplship.mappers.dhl_poland.settings import Settings
from purplship.api.proxy import Proxy as BaseProxy


class Proxy(RatingMixinProxy, BaseProxy):
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

    def get_rates(self, request: Serializable) -> Deserializable:
        return super().get_rates(request)

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
