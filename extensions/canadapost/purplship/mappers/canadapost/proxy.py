import base64
from typing import List
from purplship.core.errors import PurplShipError
from purplship.core.utils.serializable import Serializable, Deserializable
from purplship.core.utils.pipeline import Pipeline, Job
from purplship.core.utils import (
    to_xml,
    request as http,
    exec_parrallel,
    bundle_xml,
)
from purplship.mappers.canadapost.settings import Settings
from purplship.api.proxy import Proxy as BaseProxy
from pycanadapost.rating import mailing_scenario


class Proxy(BaseProxy):
    settings: Settings

    def get_rates(self, request: Serializable[mailing_scenario]) -> Deserializable[str]:
        response = http(
            url=f"{self.settings.server_url}/rs/ship/price",
            data=bytearray(request.serialize(), "utf-8"),
            headers={
                "Content-Type": "application/vnd.cpc.ship.rate-v4+xml",
                "Accept": "application/vnd.cpc.ship.rate-v4+xml",
                "Authorization": f"Basic {self.settings.authorization}",
                "Accept-language": "en-CA",
            },
            method="POST",
        )
        return Deserializable(response, to_xml)

    def get_tracking(self, request: Serializable[List[str]]) -> Deserializable[str]:
        """
        get_tracking make parallel request for each pin
        """

        def track(tracking_pin: str) -> str:
            return http(
                url=f"{self.settings.server_url}/vis/track/pin/{tracking_pin}/summary",
                headers={
                    "Accept": "application/vnd.cpc.track+xml",
                    "Authorization": f"Basic {self.settings.authorization}",
                    "Accept-language": "en-CA",
                },
                method="GET",
            )

        response: List[str] = exec_parrallel(track, request.serialize())

        return Deserializable(bundle_xml(xml_strings=response), to_xml)

    def create_shipment(self, request: Serializable[Pipeline]) -> Deserializable[str]:
        def _contract_shipment(job: Job):
            return http(
                url=f"{self.settings.server_url}/rs/{self.settings.customer_number}/{self.settings.customer_number}/shipment",
                data=bytearray(job.data.serialize(), "utf-8"),
                headers={
                    "Content-Type": "application/vnd.cpc.shipment-v8+xml",
                    "Accept": "application/vnd.cpc.shipment-v8+xml",
                    "Authorization": f"Basic {self.settings.authorization}",
                    "Accept-language": "en-CA",
                },
                method="POST",
            )

        def _non_contract_shipment(job: Job):
            return http(
                url=f"{self.settings.server_url}/rs/{self.settings.customer_number}/ncshipment",
                data=bytearray(job.data.serialize(), "utf-8"),
                headers={
                    "Accept": "application/vnd.cpc.ncshipment-v4+xml",
                    "Content-Type": "application/vnd.cpc.ncshipment-v4+xml",
                    "Authorization": f"Basic {self.settings.authorization}",
                    "Accept-language": "en-CA",
                },
                method="POST",
            )

        def _get_label(job: Job):
            label_string = http(
                decoder=lambda b: base64.encodebytes(b).decode("utf-8"),
                url=job.data,
                headers={
                    "Accept": "application/pdf",
                    "Authorization": f"Basic {self.settings.authorization}",
                },
                method="GET",
            )
            return f"<label>{label_string}</label>"

        def process(job: Job):
            if job.data is None:
                return job.fallback

            subprocess = {
                "contract_shipment": _contract_shipment,
                "non_contract_shipment": _non_contract_shipment,
                "shipment_label": _get_label,
            }
            if job.id not in subprocess:
                raise PurplShipError(f"Unknown shipment request job id: {job.id}")

            return subprocess[job.id](job)

        pipeline: Pipeline = request.serialize()
        response = pipeline.apply(process)

        return Deserializable(bundle_xml(response), to_xml)

    def schedule_pickup(self, request: Serializable[Pipeline]) -> Deserializable[str]:
        def _availability(job: Job) -> str:
            return http(
                url=f"{self.settings.server_url}/ad/pickup/pickupavailability/{job.data}",
                headers={
                    "Accept": "application/vnd.cpc.pickup+xml",
                    "Authorization": f"Basic {self.settings.authorization}",
                    "Accept-language": "en-CA",
                },
                method="GET",
            )

        def _create_pickup(job: Job) -> str:
            return http(
                url=f"{self.settings.server_url}/enab/{self.settings.customer_number}/pickuprequest",
                data=bytearray(job.data.serialize(), "utf-8"),
                headers={
                    "Accept": "application/vnd.cpc.pickuprequest+xml",
                    "Content-Type": "application/vnd.cpc.pickuprequest+xml",
                    "Authorization": f"Basic {self.settings.authorization}",
                    "Accept-language": "en-CA",
                },
                method="POST",
            )

        def process(job: Job):
            if job.data is None:
                return job.fallback

            subprocess = {
                "create_pickup": _create_pickup,
                "availability": _availability,
            }
            if job.id not in subprocess:
                raise PurplShipError(f"Unknown pickup request job id: {job.id}")

            return subprocess[job.id](job)

        pipeline: Pipeline = request.serialize()
        response = pipeline.apply(process)

        return Deserializable(bundle_xml(response), to_xml)

    def modify_pickup(self, request: Serializable[dict]) -> Deserializable[str]:
        payload = request.serialize()
        response = http(
            url=f"{self.settings.server_url}/enab/{self.settings.customer_number}/pickuprequest/{payload['pickuprequest']}",
            data=bytearray(payload["data"], "utf-8"),
            headers={
                "Accept": "application/vnd.cpc.pickuprequest+xml",
                "Authorization": f"Basic {self.settings.authorization}",
                "Accept-language": "en-CA",
            },
            method="PUT",
        )
        return Deserializable(response, to_xml)

    def cancel_pickup(self, request: Serializable[str]) -> Deserializable[str]:
        pickuprequest = request.serialize()
        response = http(
            url=f"{self.settings.server_url}/enab/{self.settings.customer_number}/pickuprequest/{pickuprequest}",
            headers={
                "Accept": "application/vnd.cpc.pickuprequest+xml",
                "Authorization": f"Basic {self.settings.authorization}",
                "Accept-language": "en-CA",
            },
            method="DELETE",
        )
        return Deserializable(response or "<wrapper></wrapper>", to_xml)
