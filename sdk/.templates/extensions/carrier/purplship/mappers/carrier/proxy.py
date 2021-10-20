from typing import Any
from purplship.core.utils import XP, request as http, Serializable, Deserializable
from purplship.api.proxy import Proxy as BaseProxy
from purplship.mappers.carrier.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    """ Proxy Methods """

    # def validate_address(self, request: Serializable) -> Deserializable[str]:
    #     response = self._send_request(request)
    #
    #     return Deserializable(response, XP.to_xml)

    def get_rates(self, request: Serializable) -> Deserializable[str]:
        response = self._send_request(request)

        return Deserializable(response, XP.to_xml)

    # def get_tracking(
    #     self, request: Serializable
    # ) -> Deserializable[str]:
    #     response = self._send_request(request)
    #
    #     return Deserializable(response, XP.to_xml)
    #
    # def create_shipment(
    #     self, request: Serializable
    # ) -> Deserializable[str]:
    #     response = self._send_request(request)
    #
    #     return Deserializable(response, XP.to_xml)
    #
    # def schedule_pickup(
    #     self, request: Serializable
    # ) -> Deserializable[str]:
    #     response = self._send_request(request)
    #
    #     return Deserializable(response, XP.to_xml)
    #
    # def modify_pickup(
    #     self, request: Serializable
    # ) -> Deserializable[str]:
    #     response = self._send_request(request)
    #
    #     return Deserializable(response, XP.to_xml)
    #
    # def cancel_pickup(
    #     self, request: Serializable
    # ) -> Deserializable[str]:
    #     response = self._send_request(request)
    #
    #     return Deserializable(response, XP.to_xml)

    """ Private Methods """

    def _send_request(self, request: Serializable[Any]) -> str:
        return http(
            url=self.settings.server_url,
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )

