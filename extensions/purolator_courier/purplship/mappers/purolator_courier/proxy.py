import logging
from typing import Any
from pysoap.envelope import Envelope
from purplship.core.utils import to_xml, request as http, bundle_xml, Pipeline, Job
from purplship.api.proxy import Proxy as BaseProxy
from purplship.mappers.purolator_courier.settings import Settings
from purplship.core.utils.serializable import Serializable, Deserializable

logger = logging.getLogger(__name__)

SHIPPING_SERVICES = dict(
    create=dict(
        path="/EWS/V2/Shipping/ShippingService.asmx",
        action="http://purolator.com/pws/service/v2/CreateShipment"
    ),
    validate=dict(
        path="/EWS/V2/Shipping/ShippingService.asmx",
        action="http://purolator.com/pws/service/v2/ValidateShipment"
    ),
    document=dict(
        path="/EWS/V1/ShippingDocuments/ShippingDocumentsService.asmx",
        action="http://purolator.com/pws/service/v1/GetDocuments"
    )
)


class Proxy(BaseProxy):
    settings: Settings

    def _send_request(self, path: str, soapaction: str, request: Serializable[Any]) -> str:
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

    def get_rates(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = http(
            url=f"{self.settings.server_url}/EWS/V2/Estimating/EstimatingService.asmx",
            data=bytearray(request.serialize(), "utf-8"),
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "soapaction": "http://purolator.com/pws/service/v2/GetFullEstimate",
                "Authorization": f"Basic {self.settings.authorization}",
            },
            method="POST",
        )
        return Deserializable(response, to_xml)

    def get_tracking(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = http(
            url=f"{self.settings.server_url}/PWS/V1/Tracking/TrackingService.asmx",
            data=request.serialize().encode("utf-8"),
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "soapaction": "http://purolator.com/pws/service/v1/TrackPackagesByPin",
                "Authorization": f"Basic {self.settings.authorization}",
            },
            method="POST",
        )
        return Deserializable(response, to_xml)

    def create_shipment(self, request: Serializable[Pipeline]) -> Deserializable[str]:
        def process(job: Job):
            return (
                http(
                    url=f"{self.settings.server_url}{SHIPPING_SERVICES[job.id]['path']}",
                    data=bytearray(job.data, "utf-8"),
                    headers={
                        "Content-Type": "text/xml; charset=utf-8",
                        "soapaction": SHIPPING_SERVICES[job.id]['action'],
                        "Authorization": f"Basic {self.settings.authorization}",
                    },
                    method="POST",
                )
                if job.data is not None else job.fallback
            )

        pipeline: Pipeline = request.serialize()
        _, *response = pipeline.apply(process)
        return Deserializable(bundle_xml(response), to_xml)

    def request_pickup(self, request: Serializable[Pipeline]) -> Deserializable[str]:

        def process(job: Job):
            if job.data is None:
                return job.fallback

            return self._send_request(
                path='/EWS/V1/PickUp/PickUpService.asmx',
                request=job.data,
                soapaction=dict(
                    validate="http://purolator.com/pws/service/v1/ValidatePickUp",
                    schedule="http://purolator.com/pws/service/v1/SchedulePickUp"
                )[job.id]
            )

        pipeline: Pipeline = request.serialize()
        response = pipeline.apply(process)

        return Deserializable(bundle_xml(response), to_xml)

    def modify_pickup(self, request: Serializable[Pipeline]) -> Deserializable[str]:

        def process(job: Job):
            if job.data is None:
                return job.fallback

            return self._send_request(
                path='/EWS/V1/PickUp/PickUpService.asmx',
                request=job.data,
                soapaction=dict(
                    validate="http://purolator.com/pws/service/v1/ValidatePickUp",
                    modify="http://purolator.com/pws/service/v1/ModifyPickUp"
                )[job.id]
            )

        pipeline: Pipeline = request.serialize()
        response = pipeline.apply(process)

        return Deserializable(bundle_xml(response), to_xml)

    def cancel_pickup(self, request: Serializable[Envelope]) -> Deserializable[str]:
        response = self._send_request(
            path='/EWS/V1/PickUp/PickUpService.asmx',
            soapaction='http://purolator.com/pws/service/v1/VoidPickUp',
            request=request
        )

        return Deserializable(response, to_xml)
