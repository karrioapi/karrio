from typing import List, Any
from ups_lib.av_request import AddressValidationRequest
from purplship.core.utils import (
    XP,
    request as http,
    exec_parrallel,
    Serializable,
    Deserializable,
    Envelope,
    Pipeline,
    Job
)
from purplship.api.proxy import Proxy as BaseProxy
from purplship.mappers.ups.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    def _send_request(self, path: str, request: Serializable[Any]) -> str:
        return http(
            url=f"{self.settings.server_url}{path}",
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )

    def validate_address(self, request: Serializable[AddressValidationRequest]) -> Deserializable[str]:
        response = self._send_request("/AV", request)

        return Deserializable(response, XP.to_xml)

    def get_rates(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request("/Rate", request)

        return Deserializable(response, XP.to_xml)

    def get_tracking(
        self, request: Serializable[List[Envelope]]
    ) -> Deserializable[str]:
        """
        get_tracking make parallel request for each TrackRequest
        """

        def get_tracking(track_request: str):
            return self._send_request("/Track", Serializable(track_request))

        response: List[str] = exec_parrallel(get_tracking, request.serialize())

        return Deserializable(XP.bundle_xml(xml_strings=response), XP.to_xml)

    def create_shipment(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request("/Ship", request)

        return Deserializable(response, XP.to_xml)

    def cancel_shipment(self, request: Serializable) -> Deserializable[str]:
        response = self._send_request("/Ship", request)

        return Deserializable(response, XP.to_xml)

    def schedule_pickup(self, request: Serializable[Pipeline]) -> Deserializable[str]:
        def process(job: Job):
            if job.data is None:
                return job.fallback

            return self._send_request("/Pickup", job.data)

        pipeline: Pipeline = request.serialize()
        response = pipeline.apply(process)

        return Deserializable(XP.bundle_xml(response), XP.to_xml)

    def modify_pickup(self, request: Serializable[Pipeline]) -> Deserializable[str]:
        def process(job: Job):
            if job.data is None:
                return job.fallback

            return self._send_request("/Pickup", job.data)

        pipeline: Pipeline = request.serialize()
        response = pipeline.apply(process)

        return Deserializable(XP.bundle_xml(response), XP.to_xml)

    def cancel_pickup(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request("/Pickup", request)

        return Deserializable(response, XP.to_xml)
