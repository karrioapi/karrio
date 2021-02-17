import urllib.parse
from usps_lib.track_field_request import TrackFieldRequest

from purplship.api.proxy import Proxy as BaseProxy
from purplship.core.utils import Serializable, Deserializable, XP, request as http
from purplship.mappers.usps.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    """ Proxy interface method implementations """

    def get_tracking(self, request: Serializable[TrackFieldRequest]) -> Deserializable[str]:
        query = urllib.parse.urlencode({"API": "TrackV2", "XML": request.serialize()})
        response = http(url=f"{self.settings.server_url}?{query}", method="GET")

        return Deserializable(response, XP.to_xml)
