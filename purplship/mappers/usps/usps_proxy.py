from io import StringIO
from typing import List, Union
from gds_helpers import export, to_xml, request as http
from purplship.mappers.usps.usps_mapper import USPSMapper
from purplship.mappers.usps.usps_client import USPSClient
from purplship.domain.proxy import Proxy

from functools import reduce

class USPSProxy(Proxy):

    def __init__(self, client: USPSClient, mapper: USPSMapper = None):
        self.client = client
        self.mapper = USPSMapper(client) if mapper is None else mapper

    """ Proxy interface methods """

    def get_quotes(self, rate_request: '') -> "XMLElement":
        pass

    def get_trackings(self, tracking_request: '') -> "XMLElement":
        pass
