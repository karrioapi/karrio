from typing import Any
from fedex_lib.ship_service_v26 import TrackingId
from karrio.core.utils import (
    XP,
    request as http,
    Pipeline,
    Serializable,
    Deserializable,
    Job,
    Envelope,
)
from karrio.api.proxy import Proxy as BaseProxy
from karrio.mappers.fedex.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    def _send_request(self, path: str, request: Serializable[Any]) -> str:
        return http(
            url=f"{self.settings.server_url}{path}",
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )

    def validate_address(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request("/addressvalidation", request)

        return Deserializable(response, XP.to_xml)

    def get_rates(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request("/rate", request)

        return Deserializable(response, XP.to_xml)

    def get_tracking(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request("/track", request)

        return Deserializable(response, XP.to_xml)

    def create_shipment(self, request: Serializable[Envelope]) -> Deserializable[str]:

        requests = request.serialize()
        response = self._send_request("/ship", Serializable(requests[0]))
        master_id = XP.find(
            "MasterTrackingId", XP.to_xml(response), TrackingId, first=True
        )

        if len(requests) > 1 and master_id is not None:
            responses = [
                self._send_request(
                    "/ship",
                    Serializable(
                        request.replace(
                            "[MASTER_ID_TYPE]", master_id.TrackingIdType
                        ).replace("[MASTER_TRACKING_ID]", master_id.TrackingNumber)
                    ),
                )
                for request in requests[1:]
            ]
            return Deserializable(XP.bundle_xml([response, *responses]), XP.to_xml)

        return Deserializable(response, XP.to_xml)

    def cancel_shipment(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request("/ship", request)

        return Deserializable(response, XP.to_xml)

    def schedule_pickup(self, request: Serializable[Pipeline]) -> Deserializable[str]:
        def process(job: Job):
            if job.data is None:
                return job.fallback

            return self._send_request("/pickup", job.data)

        pipeline: Pipeline = request.serialize()
        response = pipeline.apply(process)

        return Deserializable(XP.bundle_xml(response), XP.to_xml)

    def modify_pickup(self, request: Serializable[Pipeline]) -> Deserializable[str]:
        def process(job: Job):
            if job.data is None:
                return job.fallback

            return self._send_request("/pickup", job.data)

        pipeline: Pipeline = request.serialize()
        response = pipeline.apply(process)

        return Deserializable(XP.bundle_xml(response), XP.to_xml)

    def cancel_pickup(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request("/pickup", request)

        return Deserializable(response, XP.to_xml)
