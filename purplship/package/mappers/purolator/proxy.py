from purplship.core.utils.helpers import to_xml, request as http
from purplship.package.proxy import Proxy as BaseProxy
from purplship.package.mappers.ups.settings import Settings
from purplship.core.utils.serializable import Serializable, Deserializable
from purplship.core.utils.xml import Element


class Proxy(BaseProxy):
    settings: Settings

    def get_rates(self, request: Serializable[Element]) -> Deserializable[str]:
        response = http(
            url=f"{self.settings.server_url}/EWS/V2/Estimating/EstimatingService.asmx",
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)

    def get_tracking(self, request: Serializable[Element]) -> Deserializable[str]:
        response = http(
            url=f"{self.settings.server_url}/PWS/V1/Tracking/TrackingService.asmx",
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)

    def create_shipment(self, request: Serializable[Element]) -> Deserializable[str]:
        response = http(
            url=f"{self.settings.server_url}/EWS/V2/Shipping/ShippingService.asmx",
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)
