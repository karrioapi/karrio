from typing import List, Any, Tuple
from ups_lib.av_request import AddressValidationRequest
from karrio.core.utils import (
    XP,
    DP,
    request as http,
    exec_parrallel,
    Serializable,
    Deserializable,
    Envelope,
    Pipeline,
    Job,
)
from karrio.api.proxy import Proxy as BaseProxy
from karrio.mappers.ups.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    def _send_request(self, path: str, request: Serializable[Any]) -> str:
        return http(
            url=f"{self.settings.server_url}{path}",
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )

    def validate_address(
        self, request: Serializable[AddressValidationRequest]
    ) -> Deserializable[str]:
        response = self._send_request("/webservices/AV", request)

        return Deserializable(response, XP.to_xml)

    def get_rates(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request("/webservices/Rate", request)

        return Deserializable(response, XP.to_xml)

    def get_tracking(
        self, request: Serializable[List[str]]
    ) -> Deserializable[List[Tuple[str, dict]]]:
        """
        get_tracking makes parallel requests for each tracking number
        """

        def get_tracking(tracking_number: str):
            return tracking_number, http(
                url=f"{self.settings.server_url}/track/v1/details/{tracking_number}",
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "AccessLicenseNumber": self.settings.access_license_number,
                    "Username": self.settings.username,
                    "Password": self.settings.password,
                },
                method="GET",
            )

        responses: List[str] = exec_parrallel(get_tracking, request.serialize())
        return Deserializable(
            responses,
            lambda res: [
                (num, DP.to_dict(track)) for num, track in res if any(track.strip())
            ],
        )

    def create_shipment(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request("/webservices/Ship", request)

        return Deserializable(response, XP.to_xml)

    def cancel_shipment(self, request: Serializable) -> Deserializable[str]:
        response = self._send_request("/webservices/Ship", request)

        return Deserializable(response, XP.to_xml)

    def schedule_pickup(self, request: Serializable[Pipeline]) -> Deserializable[str]:
        def process(job: Job):
            if job.data is None:
                return job.fallback

            return self._send_request("/webservices/Pickup", job.data)

        pipeline: Pipeline = request.serialize()
        response = pipeline.apply(process)
        return Deserializable(XP.bundle_xml(response), XP.to_xml)

    def modify_pickup(self, request: Serializable[Pipeline]) -> Deserializable[str]:
        def process(job: Job):
            if job.data is None:
                return job.fallback

            return self._send_request("/webservices/Pickup", job.data)

        pipeline: Pipeline = request.serialize()
        response = pipeline.apply(process)

        return Deserializable(XP.bundle_xml(response), XP.to_xml)

    def cancel_pickup(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request("/webservices/Pickup", request)

        return Deserializable(response, XP.to_xml)
