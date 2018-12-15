from functools import reduce
from typing import List, Union
from gds_helpers import export, to_xml, request as http
from purplship.mappers.aramex.aramex_mapper import AramexMapper
from purplship.mappers.aramex.aramex_client import AramexClient
from purplship.domain.proxy import Proxy
from pyaramex.Tracking import ShipmentTrackingRequest
from pyaramex.Rating import RateCalculatorRequest


class AramexProxy(Proxy):

    def __init__(self, client: AramexClient, mapper: AramexMapper = None):
        self.client = client
        self.mapper = AramexMapper(client) if mapper is None else mapper

    """ Proxy interface methods """

    def get_quotes(self, rate_request: ShipmentTrackingRequest) -> "XMLElement":
        pass

    def get_trackings(self, tracking_request: RateCalculatorRequest) -> "XMLElement":
        pass
