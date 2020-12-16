import logging
from typing import Any
from pysoap.envelope import Envelope
from purplship.core.utils import XP, request as http, Pipeline, Job
from purplship.api.proxy import Proxy as BaseProxy
from purplship.mappers.purolator_courier.settings import Settings
from purplship.core.utils.serializable import Serializable, Deserializable

logger = logging.getLogger(__name__)


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
                "Authorization": f"Basic {self.settings.authorization}",
            },
            method="POST",
        )

    def validate_address(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request(
            path="/EWS/V2/ServiceAvailability/ServiceAvailabilityService.asmx",
            soapaction="http://purolator.com/pws/service/v2/ValidateCityPostalCodeZip",
            request=request,
        )

        return Deserializable(response, XP.to_xml)

    def get_rates(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request(
            path="/EWS/V2/Estimating/EstimatingService.asmx",
            soapaction="http://purolator.com/pws/service/v2/GetFullEstimate",
            request=request,
        )

        return Deserializable(response, XP.to_xml)

    def get_tracking(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request(
            path="/PWS/V1/Tracking/TrackingService.asmx",
            soapaction="http://purolator.com/pws/service/v1/TrackPackagesByPin",
            request=request,
        )

        return Deserializable(response, XP.to_xml)

    def create_shipment(self, request: Serializable[Pipeline]) -> Deserializable[str]:
        def process(job: Job):
            if job.data is None:
                return job.fallback

            return self._send_request(
                request=job.data,
                path=dict(
                    create="/EWS/V2/Shipping/ShippingService.asmx",
                    validate="/EWS/V2/Shipping/ShippingService.asmx",
                    document="/EWS/V1/ShippingDocuments/ShippingDocumentsService.asmx",
                )[job.id],
                soapaction=dict(
                    create="http://purolator.com/pws/service/v2/CreateShipment",
                    validate="http://purolator.com/pws/service/v2/ValidateShipment",
                    document="http://purolator.com/pws/service/v1/GetDocuments",
                )[job.id],
            )

        pipeline: Pipeline = request.serialize()
        _, *response = pipeline.apply(process)
        return Deserializable(XP.bundle_xml(response), XP.to_xml)

    def cancel_shipment(self, request: Serializable) -> Deserializable:
        response = self._send_request(
            path="/EWS/V2/Shipping/ShippingService.asmx",
            soapaction="http://purolator.com/pws/service/v2/VoidShipment",
            request=request,
        )

        return Deserializable(response, XP.to_xml)

    def schedule_pickup(self, request: Serializable[Pipeline]) -> Deserializable[str]:
        def process(job: Job):
            if job.data is None:
                return job.fallback

            return self._send_request(
                path="/EWS/V1/PickUp/PickUpService.asmx",
                request=job.data,
                soapaction=dict(
                    validate="http://purolator.com/pws/service/v1/ValidatePickUp",
                    schedule="http://purolator.com/pws/service/v1/SchedulePickUp",
                )[job.id],
            )

        pipeline: Pipeline = request.serialize()
        response = pipeline.apply(process)

        return Deserializable(XP.bundle_xml(response), XP.to_xml)

    def modify_pickup(self, request: Serializable[Pipeline]) -> Deserializable[str]:
        def process(job: Job):
            if job.data is None:
                return job.fallback

            return self._send_request(
                path="/EWS/V1/PickUp/PickUpService.asmx",
                request=job.data,
                soapaction=dict(
                    validate="http://purolator.com/pws/service/v1/ValidatePickUp",
                    modify="http://purolator.com/pws/service/v1/ModifyPickUp",
                )[job.id],
            )

        pipeline: Pipeline = request.serialize()
        response = pipeline.apply(process)

        return Deserializable(XP.bundle_xml(response), XP.to_xml)

    def cancel_pickup(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request(
            path="/EWS/V1/PickUp/PickUpService.asmx",
            soapaction="http://purolator.com/pws/service/v1/VoidPickUp",
            request=request,
        )

        return Deserializable(response, XP.to_xml)
