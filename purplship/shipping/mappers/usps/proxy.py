import urllib.parse
from typing import Union
from purplship.core.utils.serializable import Serializable, Deserializable
from purplship.core.utils.helpers import to_xml, request as http
from purplship.shipping.mappers.usps.settings import Settings
from purplship.shipping.proxy import Proxy as BaseProxy
from pyusps.ratev4request import RateV4Request
from pyusps.intlratev2request import IntlRateV2Request
from pyusps.trackfieldrequest import TrackFieldRequest


class Proxy(BaseProxy):
    settings: Settings

    """ Proxy interface method implementations """

    def get_rates(self, request: Serializable[Union[RateV4Request, IntlRateV2Request]]) -> Deserializable[str]:
        query = urllib.parse.urlencode(request.serialize())
        response = http(
            url=f'{self.settings.server_url}?{query}',
            method="GET",
        )
        return Deserializable(response, to_xml)

    def get_tracking(self, request: Serializable[TrackFieldRequest]) -> Deserializable[str]:
        query = urllib.parse.urlencode(request.serialize())
        response = http(
            url=f"{self.settings.server_url}?{query}",
            method="GET",
        )
        return Deserializable(response, to_xml)
