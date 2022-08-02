from fedex_lib.ship_service_v26 import TrackingId

import karrio.lib as lib
import karrio.api.proxy as proxy
from karrio.mappers.fedex.settings import Settings


class Proxy(proxy.Proxy):
    settings: Settings

    def _send_request(self, path: str, request: lib.Serializable) -> str:
        return lib.request(
            url=f"{self.settings.server_url}{path}",
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={"Content-Type": "application/xml"},
        )

    def validate_address(
        self, request: lib.Serializable[lib.Envelope]
    ) -> lib.Deserializable[str]:
        response = self._send_request("/addressvalidation", request)

        return lib.Deserializable(response, lib.to_element)

    def get_rates(
        self, request: lib.Serializable[lib.Envelope]
    ) -> lib.Deserializable[str]:
        response = self._send_request("/rate", request)

        return lib.Deserializable(response, lib.to_element)

    def get_tracking(
        self, request: lib.Serializable[lib.Envelope]
    ) -> lib.Deserializable[str]:
        response = self._send_request("/track", request)

        return lib.Deserializable(response, lib.to_element)

    def create_shipment(
        self, request: lib.Serializable[lib.Envelope]
    ) -> lib.Deserializable[str]:

        requests = request.serialize()
        response = self._send_request("/ship", lib.Serializable(requests[0]))
        master_id = lib.find_element(
            "MasterTrackingId", lib.to_element(response), TrackingId, first=True
        )

        if len(requests) > 1 and master_id is not None:
            responses = [
                self._send_request(
                    "/ship",
                    lib.Serializable(
                        request.replace(
                            "[MASTER_ID_TYPE]", master_id.TrackingIdType
                        ).replace("[MASTER_TRACKING_ID]", master_id.TrackingNumber),
                    ),
                )
                for request in requests[1:]
            ]
            return lib.Deserializable([response, *responses], lib.to_element)

        return lib.Deserializable(response, lib.to_element)

    def cancel_shipment(
        self, request: lib.Serializable[lib.Envelope]
    ) -> lib.Deserializable[str]:
        response = self._send_request("/ship", request)

        return lib.Deserializable(response, lib.to_element)

    def schedule_pickup(
        self, request: lib.Serializable[lib.Pipeline]
    ) -> lib.Deserializable[str]:
        def process(job: lib.Job):
            if job.data is None:
                return job.fallback

            return self._send_request("/pickup", job.data)

        pipeline: lib.Pipeline = request.serialize()
        response = pipeline.apply(process)

        return lib.Deserializable(response, lib.to_element)

    def modify_pickup(
        self, request: lib.Serializable[lib.Pipeline]
    ) -> lib.Deserializable[str]:
        def process(job: lib.Job):
            if job.data is None:
                return job.fallback

            return self._send_request("/pickup", job.data)

        pipeline: lib.Pipeline = request.serialize()
        response = pipeline.apply(process)

        return lib.Deserializable(response, lib.to_element)

    def cancel_pickup(
        self,
        request: lib.Serializable[lib.Envelope],
    ) -> lib.Deserializable[str]:
        response = self._send_request("/pickup", request)

        return lib.Deserializable(response, lib.to_element)

    def upload_document(
        self,
        request: lib.Serializable[lib.Envelope],
    ) -> lib.Deserializable:
        response = self._send_request("/uploaddocument", request)

        return lib.Deserializable(response, lib.to_element)
