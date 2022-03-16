import urllib.parse
from usps_lib.track_field_request import TrackFieldRequest

from karrio.api.proxy import Proxy as BaseProxy
from karrio.core.utils import Serializable, Deserializable, XP, request as http
from karrio.mappers.usps_international.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    """ Proxy interface method implementations """

    def get_tracking(self, request: Serializable[TrackFieldRequest]) -> Deserializable[str]:
        query = urllib.parse.urlencode({"API": "TrackV2", "XML": request.serialize()})
        response = http(url=f"{self.settings.server_url}?{query}", method="GET")

        return Deserializable(response, XP.to_xml)

    def get_rates(self, request: Serializable) -> Deserializable:
        query = urllib.parse.urlencode({"API": "IntlRateV2", "XML": request.serialize()})
        response = http(url=f"{self.settings.server_url}?{query}", method="GET")

        return Deserializable(response, XP.to_xml)

    def create_shipment(self, request: Serializable) -> Deserializable:
        tag = request.value.__class__.__name__.replace("Request", "")
        api = f"{tag}Certify" if self.settings.test else tag
        serialized_request = request.serialize().replace(tag, api)
        query = urllib.parse.urlencode({"API": api, "XML": serialized_request})
        response = http(url=f"{self.settings.server_url}?{query}", method="GET")

        return Deserializable(response, XP.to_xml)

    def cancel_shipment(self, request: Serializable) -> Deserializable:
        tag = request.value.__class__.__name__.replace("Request", "")
        api = f"{tag}Certify" if self.settings.test else tag
        serialized_request = request.serialize().replace(tag, api)
        query = urllib.parse.urlencode({"API": api, "XML": serialized_request})
        response = http(url=f"{self.settings.server_url}?{query}", method="GET")

        return Deserializable(response, XP.to_xml)
