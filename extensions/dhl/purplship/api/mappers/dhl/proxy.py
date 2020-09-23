from purplship.core.utils.helpers import to_xml, request as http
from purplship.core.utils.serializable import Serializable, Deserializable
from purplship.api.mappers.dhl.settings import Settings
from purplship.api.proxy import Proxy as BaseProxy
from pydhl.dct_req_global_2_0 import DCTRequest
from pydhl.tracking_request_known_1_0 import KnownTrackingRequest
from pydhl.ship_val_global_req_6_2 import ShipmentRequest
from pydhl.book_pickup_global_req_3_0 import BookPURequest
from pydhl.modify_pickup_global_req_3_0 import ModifyPURequest
from pydhl.cancel_pickup_global_req_3_0 import CancelPURequest


class Proxy(BaseProxy):
    settings: Settings

    def get_rates(self, request: Serializable[DCTRequest]) -> Deserializable[str]:
        response = http(
            url=self.settings.server_url,
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)

    def get_tracking(
        self, request: Serializable[KnownTrackingRequest]
    ) -> Deserializable[str]:
        response = http(
            url=self.settings.server_url,
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)

    def create_shipment(
        self, request: Serializable[ShipmentRequest]
    ) -> Deserializable[str]:
        response = http(
            url=self.settings.server_url,
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)

    def request_pickup(
        self, request: Serializable[BookPURequest]
    ) -> Deserializable[str]:
        response = http(
            url=self.settings.server_url,
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)

    def modify_pickup(
        self, request: Serializable[ModifyPURequest]
    ) -> Deserializable[str]:
        response = http(
            url=self.settings.server_url,
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)

    def cancel_pickup(
        self, request: Serializable[CancelPURequest]
    ) -> Deserializable[str]:
        response = http(
            url=self.settings.server_url,
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)
