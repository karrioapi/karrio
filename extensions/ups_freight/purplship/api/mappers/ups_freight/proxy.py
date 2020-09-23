from typing import List
from purplship.core.utils.helpers import (
    to_xml,
    request as http,
    bundle_xml,
    exec_parrallel,
)
from purplship.api.proxy import Proxy as BaseProxy
from purplship.api.mappers.ups_freight.settings import Settings
from purplship.core.utils.serializable import Serializable, Deserializable
from pyups.freight_rate_web_service_schema import FreightRateRequest
from pyups.track_web_service_schema import TrackRequest
from pyups.freight_ship_web_service_schema import FreightShipRequest


class Proxy(BaseProxy):
    settings: Settings

    def get_rates(
        self, request: Serializable[FreightRateRequest]
    ) -> Deserializable[str]:
        response = http(
            url=f"{self.settings.server_url}/FreightRate",
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)

    def get_tracking(
        self, request: Serializable[List[TrackRequest]]
    ) -> Deserializable[str]:
        """
        get_tracking make parrallel request for each TrackRequest
        """

        def get_tracking(track_request: str):
            return http(
                url=f"{self.settings.server_url}/Track",
                data=bytearray(track_request, "utf-8"),
                headers={"Content-Type": "application/xml"},
                method="POST",
            )

        response: List[str] = exec_parrallel(get_tracking, request.serialize())

        return Deserializable(bundle_xml(xml_strings=response), to_xml)

    def create_shipment(
        self, request: Serializable[FreightShipRequest]
    ) -> Deserializable[str]:
        response = http(
            url=f"{self.settings.server_url}/FreightShip",
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)
