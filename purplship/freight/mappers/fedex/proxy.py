from purplship.core.utils.helpers import to_xml, request as http
from purplship.freight.proxy import Proxy as BaseProxy
from purplship.freight.mappers.fedex.settings import Settings
from purplship.core.utils.serializable import Serializable, Deserializable
from pyfedex.rate_service_v26 import RateRequest
from pyfedex.ship_service_v25 import ProcessShipmentRequest
from pyfedex.pickup_service_v20 import CreatePickupRequest, CancelPickupRequest
from pyfedex.track_service_v18 import TrackRequest


class Proxy(BaseProxy):
    settings: Settings

    def get_rates(self, request: Serializable[RateRequest]) -> Deserializable[str]:
        response = http(
            url=self.settings.server_url,
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)

    def get_tracking(self, request: Serializable[TrackRequest]) -> Deserializable[str]:
        response = http(
            url=self.settings.server_url,
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)

    def create_shipment(
        self, request: Serializable[ProcessShipmentRequest]
    ) -> Deserializable[str]:
        response = http(
            url=self.settings.server_url,
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)

    def request_pickup(
        self, request: Serializable[CreatePickupRequest]
    ) -> Deserializable[str]:
        response = http(
            url=self.settings.server_url,
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)

    def cancel_pickup(
        self, request: Serializable[CancelPickupRequest]
    ) -> Deserializable[str]:
        response = http(
            url=self.settings.server_url,
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)
