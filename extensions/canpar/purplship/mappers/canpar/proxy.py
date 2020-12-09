from typing import List, Any
from purplship.core.utils import (
    Serializable,
    Deserializable,
    Envelope,
    Pipeline,
    Job,
    XP,
    request as http,
    exec_parrallel
)
from purplship.mappers.canpar.settings import Settings
from purplship.api.proxy import Proxy as BaseProxy


class Proxy(BaseProxy):
    settings: Settings

    def _send_request(
        self, path: str, soapaction: str, request: Serializable[Any]
    ) -> str:
        return http(
            url=f"{self.settings.server_url}{path}",
            data=bytearray(request.serialize(), "utf-8"),
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "soapaction": soapaction,
            },
            method="POST",
        )

    def validate_address(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request(
            path="/CanparRatingService.CanparRatingServiceHttpSoap12Endpoint/",
            soapaction="urn:searchCanadaPost",
            request=request,
        )

        return Deserializable(response, XP.to_xml)

    def get_rates(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request(
            path="/CanparRatingService.CanparRatingServiceHttpSoap12Endpoint/",
            soapaction="urn:rateShipment",
            request=request,
        )

        return Deserializable(response, XP.to_xml)

    def get_tracking(self, request: Serializable[List[Envelope]]) -> Deserializable[str]:
        """
        get_tracking make parallel request for each TrackRequest
        """

        def get_tracking(track_request: str):
            return self._send_request(
                path="/CanparAddonsService.CanparAddonsServiceHttpSoap12Endpoint/",
                soapaction="urn:trackByBarcodeV2",
                request=Serializable(track_request),
            )

        response: List[str] = exec_parrallel(get_tracking, request.serialize())

        return Deserializable(XP.bundle_xml(xml_strings=response), XP.to_xml)

    def create_shipment(self, request: Serializable[Envelope]) -> Deserializable[str]:
        def process(job: Job):
            if job.data is None:
                return job.fallback

            return self._send_request(
                path="/CanshipBusinessService.CanshipBusinessServiceHttpSoap12Endpoint/",
                request=job.data,
                soapaction=dict(
                    process="urn:processShipment",
                    get_label="urn:getLabels",
                )[job.id],
            )

        pipeline: Pipeline = request.serialize()
        response = pipeline.apply(process)

        return Deserializable(XP.bundle_xml(response), XP.to_xml)

    def cancel_shipment(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request(
            path="/CanshipBusinessService.CanshipBusinessServiceHttpSoap12Endpoint/",
            soapaction="urn:voidShipment",
            request=request,
        )

        return Deserializable(response, XP.to_xml)

    def schedule_pickup(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request(
            path="/CanparAddonsService.CanparAddonsServiceHttpSoap12Endpoint/",
            soapaction="urn:schedulePickupV2",
            request=request,
        )

        return Deserializable(response, XP.to_xml)

    def modify_pickup(self, request: Serializable[Envelope]) -> Deserializable[str]:
        def process(job: Job):
            if job.data is None:
                return job.fallback

            return self._send_request(
                path="/CanparAddonsService.CanparAddonsServiceHttpSoap12Endpoint/",
                request=job.data,
                soapaction=dict(
                    cancel="urn:cancelPickup",
                    schedule="urn:schedulePickupV2",
                )[job.id],
            )

        pipeline: Pipeline = request.serialize()
        response = pipeline.apply(process)

        return Deserializable(XP.bundle_xml(response), XP.to_xml)

    def cancel_pickup(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request(
            path="/CanparAddonsService.CanparAddonsServiceHttpSoap12Endpoint/",
            soapaction="urn:cancelPickup",
            request=request,
        )

        return Deserializable(response, XP.to_xml)
