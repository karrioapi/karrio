from typing import Any
from purplship.core.utils import XP, request as http, Serializable, Deserializable
from purplship.api.proxy import Proxy as BaseProxy
from dhl_express_lib.dct_req_global_2_0 import DCTRequest
from dhl_express_lib.tracking_request_known_1_0 import KnownTrackingRequest
from dhl_express_lib.ship_val_global_req_6_2 import ShipmentRequest
from dhl_express_lib.book_pickup_global_req_3_0 import BookPURequest
from dhl_express_lib.modify_pickup_global_req_3_0 import ModifyPURequest
from dhl_express_lib.cancel_pickup_global_req_3_0 import CancelPURequest
from dhl_express_lib.routing_global_req_2_0 import RouteRequest
from purplship.mappers.dhl_express.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    def _send_request(self, request: Serializable[Any]) -> str:
        return http(
            url=self.settings.server_url,
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )

    def validate_address(self, request: Serializable[RouteRequest]) -> Deserializable[str]:
        response = self._send_request(request)

        return Deserializable(response, XP.to_xml)

    def get_rates(self, request: Serializable[DCTRequest]) -> Deserializable[str]:
        response = self._send_request(request)

        return Deserializable(response, XP.to_xml)

    def get_tracking(
        self, request: Serializable[KnownTrackingRequest]
    ) -> Deserializable[str]:
        response = self._send_request(request)

        return Deserializable(response, XP.to_xml)

    def create_shipment(
        self, request: Serializable[ShipmentRequest]
    ) -> Deserializable[str]:
        response = self._send_request(request)

        return Deserializable(response, XP.to_xml)

    def schedule_pickup(
        self, request: Serializable[BookPURequest]
    ) -> Deserializable[str]:
        response = self._send_request(request)

        return Deserializable(response, XP.to_xml)

    def modify_pickup(
        self, request: Serializable[ModifyPURequest]
    ) -> Deserializable[str]:
        response = self._send_request(request)

        return Deserializable(response, XP.to_xml)

    def cancel_pickup(
        self, request: Serializable[CancelPURequest]
    ) -> Deserializable[str]:
        response = self._send_request(request)

        return Deserializable(response, XP.to_xml)
