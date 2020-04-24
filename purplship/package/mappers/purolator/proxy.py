import logging
from typing import cast
from purplship.core.utils.helpers import to_xml, request as http, bundle_xml
from purplship.core.utils.pipeline import Pipeline, Job as BaseJob
from purplship.package.proxy import Proxy as BaseProxy
from purplship.package.mappers.purolator.settings import Settings
from purplship.core.utils.serializable import Serializable, Deserializable
from pysoap.envelope import Envelope

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


class Job(BaseJob):
    @property
    def service(self): return


class Proxy(BaseProxy):
    settings: Settings

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
                    url=f"{self.settings.server_url}{SHIPPING_SERVICES[job.service]['path']}",
                    data=bytearray(job.data, "utf-8"),
                    headers={
                        "Content-Type": "text/xml; charset=utf-8",
                        "soapaction": SHIPPING_SERVICES[job.service]['action'],
                        "Authorization": f"Basic {self.settings.authorization}",
                    },
                    method="POST",
                )
                if job.data is not None else job.fallback
            )

        pipeline: Pipeline = request.serialize()
        _, *response = pipeline.apply(lambda _: process(cast(Job, _)))
        return Deserializable(bundle_xml(response), to_xml)
