import urllib.parse
from lxml import etree
from typing import Union
from gds_helpers import export, to_xml, request as http
from purplship.mappers.usps.usps_mapper import USPSMapper
from purplship.mappers.usps.usps_client import USPSClient
from purplship.domain.proxy import Proxy
from pyusps.ratev4request import RateV4Request
from pyusps.intlratev2request import IntlRateV2Request
from pyusps.trackfieldrequest import TrackFieldRequest


class USPSProxy(Proxy):
    def __init__(self, client: USPSClient, mapper: USPSMapper = None):
        self.client: USPSClient = client
        self.mapper: USPSMapper = USPSMapper(client) if mapper is None else mapper

    """ Proxy interface method implementations """

    def get_quotes(
        self, rate_request: Union[RateV4Request, IntlRateV2Request]
    ) -> etree.ElementBase:
        api = "RateV4" if isinstance(rate_request, RateV4Request) else "IntlRateV2"
        query = urllib.parse.urlencode({'API': api, 'XML': export(rate_request)})
        response = http(
            url=f'{self.client.server_url}?{query}',
            method="GET",
        )
        return to_xml(response)

    def get_tracking(self, tracking_request: TrackFieldRequest) -> etree.ElementBase:
        query = urllib.parse.urlencode({'API': 'TrackV2', 'XML': export(tracking_request)})
        response = http(
            url=f"{self.client.server_url}?{query}",
            method="GET",
        )
        return to_xml(response)
