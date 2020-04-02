from typing import Dict, Callable
from purplship.core.utils.helpers import to_xml, request as http, bundle_xml
from purplship.package.proxy import Proxy as BaseProxy
from purplship.package.mappers.ups.settings import Settings
from purplship.core.utils.serializable import Serializable, Deserializable
from pysoap.envelope import Envelope

SHIPPING_SERVICES = dict(
    shipping="/EWS/V2/Shipping/ShippingService.asmx",
    document="/PWS/V1/ShippingDocuments/ShippingDocumentsService.asmx",
)


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

    def create_shipment(
        self, request: Serializable[Dict[str, Callable]]
    ) -> Deserializable[str]:
        def apply(
            data: str = None, fallback: str = None, service: str = "shipping"
        ) -> str:
            return (
                http(
                    url=f"{self.settings.server_url}{SHIPPING_SERVICES[service]}",
                    data=bytearray(data, "utf-8"),
                    headers={"Content-Type": "application/xml"},
                    method="POST",
                )
                if data
                else fallback
            )

        requests: Dict[str, Callable] = request.serialize()
        validate_response = apply(**requests.get("validate")())
        create_response = apply(**requests.get("create")(validate_response))
        document_response = apply(**requests.get("document")(create_response))

        return Deserializable(bundle_xml([create_response, document_response]), to_xml)
