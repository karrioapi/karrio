from typing import Any
from pyfedex.rate_service_v26 import RateRequest
from pyfedex.ship_service_v25 import ProcessShipmentRequest
from pyfedex.track_service_v18 import TrackRequest
from pyfedex.pickup_service_v20 import CancelPickupRequest
from purplship.core.utils import (
    to_xml, request as http, Pipeline, Serializable, Deserializable, Job, bundle_xml
)
from purplship.api.proxy import Proxy as BaseProxy
from purplship.mappers.fedex_express.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    def _send_request(self, path: str, request: Serializable[Any]) -> str:
        return http(
            url=f"{self.settings.server_url}{path}",
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )

    def get_rates(self, request: Serializable[RateRequest]) -> Deserializable[str]:
        response = self._send_request('/rate', request)

        return Deserializable(response, to_xml)

    def get_tracking(self, request: Serializable[TrackRequest]) -> Deserializable[str]:
        response = self._send_request('/track', request)

        return Deserializable(response, to_xml)

    def create_shipment(
        self, request: Serializable[ProcessShipmentRequest]
    ) -> Deserializable[str]:
        response = self._send_request('/ship', request)

        return Deserializable(response, to_xml)

    def request_pickup(self, request: Serializable[Pipeline]) -> Deserializable[str]:

        def process(job: Job):
            if job.data is None:
                return job.fallback

            return self._send_request('/pickup', job.data)

        pipeline: Pipeline = request.serialize()
        response = pipeline.apply(process)

        return Deserializable(bundle_xml(response), to_xml)

    def modify_pickup(self, request: Serializable[Pipeline]) -> Deserializable[str]:

        def process(job: Job):
            if job.data is None:
                return job.fallback

            return self._send_request('/pickup', job.data)

        pipeline: Pipeline = request.serialize()
        response = pipeline.apply(process)

        return Deserializable(bundle_xml(response), to_xml)

    def cancel_pickup(self, request: Serializable[CancelPickupRequest]) -> Deserializable[str]:
        response = self._send_request('/pickup', request)

        return Deserializable(response, to_xml)
