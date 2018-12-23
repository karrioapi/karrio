from io import StringIO
from typing import List, Union
from gds_helpers import export, to_xml, request as http
from purplship.mappers.purolator.purolator_mapper import PurolatorMapper
from purplship.mappers.purolator.purolator_client import PurolatorClient
from purplship.domain.proxy import Proxy

from functools import reduce

class PurolatorProxy(Proxy):

    def __init__(self, client: PurolatorClient, mapper: PurolatorMapper = None):
        self.client = client
        self.mapper = PurolatorMapper(client) if mapper is None else mapper

    """ Proxy interface methods """

    def get_quotes(self, rate_request: '') -> "XMLElement":
        pass

    def get_trackings(self, tracking_request: '') -> "XMLElement":
        pass
