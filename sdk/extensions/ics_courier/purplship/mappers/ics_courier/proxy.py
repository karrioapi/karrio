import base64
from typing import Any
from purplship.api.proxy import Proxy as BaseProxy
from purplship.core.utils import Serializable, Deserializable, Envelope, XP, request as http
from purplship.mappers.ics_courier.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    def _send_request(
        self, soapaction: str, request: Serializable[Any]
    ) -> str:
        return http(
            url=self.settings.server_url,
            data=bytearray(request.serialize(), "utf-8"),
            headers={
                "Content-Type": "application/soap+xml; charset=utf-8",
                "soapaction": soapaction,
            },
            method="POST",
        )

    def validate_address(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request(
            soapaction="http://www.icscourier.ca/ValidateShipToInfo",
            request=request,
        )

        return Deserializable(response, XP.to_xml)

    def get_rates(self, request: Serializable[Envelope]) -> Deserializable[str]:
        product, data = request.serialize()
        responses = [
            f'<product>{product}</product>',
            self._send_request(
                soapaction="http://www.icscourier.ca/GetEstimatedCharges",
                request=Serializable(data),
            )
        ]

        return Deserializable(XP.bundle_xml(responses), XP.to_xml)

    def get_tracking(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request(
            soapaction="http://www.icscourier.ca/TracePackge",
            request=request,
        )

        return Deserializable(response, XP.to_xml)

    def create_shipment(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request(
            soapaction="http://www.icscourier.ca/CreateShipment",
            request=request,
        )

        labelURL = XP.find(XP.to_xml(response), "PackageIDAndLink", first=True)
        if labelURL is not None:
            label = http(labelURL, decoder=lambda b: base64.encodebytes(b).decode("utf-8"))
            responses = [f'<label>{label}</label>', response]

            return Deserializable(XP.bundle_xml(responses), XP.to_xml)

        return Deserializable(response, XP.to_xml)

    def cancel_shipment(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request(
            soapaction="http://www.icscourier.ca/VoidPackages",
            request=request,
        )

        return Deserializable(response, XP.to_xml)

    def schedule_pickup(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request(
            soapaction="http://www.icscourier.ca/CreatePickupRequest",
            request=request,
        )

        return Deserializable(response, XP.to_xml)

    def modify_pickup(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request(
            soapaction="http://www.icscourier.ca/CreatePickupRequest",
            request=request,
        )

        return Deserializable(response, XP.to_xml)

    def cancel_pickup(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request(
            soapaction="http://www.icscourier.ca/CreatePickupRequest",
            request=request,
        )

        return Deserializable(response, XP.to_xml)
