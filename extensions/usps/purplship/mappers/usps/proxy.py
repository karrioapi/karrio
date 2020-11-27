import urllib.parse
from typing import Union
from pyusps.rate_v4_request import RateV4Request
from pyusps.intl_rate_v2_request import IntlRateV2Request
from pyusps.track_field_request import TrackFieldRequest

from purplship.api.proxy import Proxy as BaseProxy
from purplship.core.utils.serializable import Serializable, Deserializable
from purplship.core.utils.helpers import to_xml, request as http
from purplship.mappers.usps.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    """ Proxy interface method implementations """

    def get_rates(
        self, request: Serializable[Union[RateV4Request, IntlRateV2Request]]
    ) -> Deserializable[str]:
        query = urllib.parse.urlencode(request.serialize())
        response = http(url=f"{self.settings.server_url}?{query}", method="GET")
        return Deserializable(response, to_xml)

    def get_tracking(
        self, request: Serializable[TrackFieldRequest]
    ) -> Deserializable[str]:
        query = urllib.parse.urlencode(request.serialize())
        response = http(url=f"{self.settings.server_url}?{query}", method="GET")
        return Deserializable(response, to_xml)
