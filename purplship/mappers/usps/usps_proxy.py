from io import StringIO
from lxml import etree
from typing import List, Union
from gds_helpers import export, to_xml, request as http
from purplship.mappers.usps.usps_mapper import USPSMapper
from purplship.mappers.usps.usps_client import USPSClient
from purplship.domain.proxy import Proxy
from pyusps.RateV4Request import RateV4Request
from pyusps.IntlRateV2Request import IntlRateV2Request
from pyusps.TrackRequest import TrackRequest

from functools import reduce

class USPSProxy(Proxy):

    def __init__(self, client: USPSClient, mapper: USPSMapper = None):
        self.client = client
        self.mapper = USPSMapper(client) if mapper is None else mapper

    """ Proxy interface methods """

    def get_quotes(self, rate_request: Union[RateV4Request, IntlRateV2Request]) -> etree.ElementBase:
        pass

    def get_tracking(self, TrackingRequest: TrackRequest) -> etree.ElementBase:
        pass
