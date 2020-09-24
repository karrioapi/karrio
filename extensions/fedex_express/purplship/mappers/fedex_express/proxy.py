from purplship.core.utils.helpers import to_xml, request as http
from purplship.core.utils.serializable import Serializable, Deserializable
from pyfedex.rate_service_v26 import RateRequest
from pyfedex.ship_service_v25 import ProcessShipmentRequest
from pyfedex.track_service_v18 import TrackRequest
from purplship.api.proxy import Proxy as BaseProxy
from purplship.mappers.fedex_express.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    def get_rates(self, request: Serializable[RateRequest]) -> Deserializable[str]:
        response = http(
            url=f"{self.settings.server_url}/rate",
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)

    def get_tracking(self, request: Serializable[TrackRequest]) -> Deserializable[str]:
        response = http(
            url=f"{self.settings.server_url}/track",
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)

    def create_shipment(
        self, request: Serializable[ProcessShipmentRequest]
    ) -> Deserializable[str]:
        response = http(
            url=f"{self.settings.server_url}/ship",
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)
