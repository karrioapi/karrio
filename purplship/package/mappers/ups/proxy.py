from typing import List
from purplship.core.utils.helpers import to_xml, request as http, bundle_xml, exec_parrallel
from purplship.package.proxy import Proxy as BaseProxy
from purplship.package.mappers.ups.settings import Settings
from purplship.core.utils.serializable import Serializable, Deserializable
from pyups.package_rate import RateRequest
from pyups.package_track import TrackRequest
from pyups.package_ship import ShipmentRequest


class Proxy(BaseProxy):
    settings: Settings

    def get_rates(self, request: Serializable[RateRequest]) -> Deserializable[str]:
        response = http(
            url=f"{self.settings.server_url}/Rate",
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)

    def get_tracking(self, request: Serializable[List[TrackRequest]]) -> Deserializable[str]:
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

        response = exec_parrallel(get_tracking, request.serialize())

        return Deserializable(bundle_xml(xml_strings=response), to_xml)

    def create_shipment(self, request: Serializable[ShipmentRequest]) -> Deserializable[str]:
        response = http(
            url=f"{self.settings.server_url}/Ship",
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)
