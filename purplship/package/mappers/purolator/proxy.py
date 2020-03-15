from typing import Dict
from purplship.core.utils.helpers import to_xml, request as http, to_dict
from purplship.package.proxy import Proxy as BaseProxy
from purplship.package.mappers.ups.settings import Settings
from purplship.core.utils.serializable import Serializable, Deserializable
from pysoap.envelope import Envelope


class Proxy(BaseProxy):
    settings: Settings

    def get_rates(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = http(
            url=f"{self.settings.server_url}/EWS/V2/Estimating/EstimatingService.asmx",
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)

    def get_tracking(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = http(
            url=f"{self.settings.server_url}/PWS/V1/Tracking/TrackingService.asmx",
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)

    def create_shipment(self, request: Serializable[Dict[str, Envelope]]) -> Deserializable[str]:
        def apply(data):
            return http(
                url=f"{self.settings.server_url}/EWS/V2/Shipping/ShippingService.asmx",
                data=bytearray(data, "utf-8"),
                headers={"Content-Type": "application/xml"},
                method="POST",
            )
        serialized_requests: Dict[str, str] = request.serialize()
        valid = apply(serialized_requests.get('validate'))

        if str(to_dict(valid)) == str(True):
            response = apply(serialized_requests.get('create'))
            return Deserializable(response, to_xml)

        return Deserializable(serialized_requests.get('error'), to_xml)
