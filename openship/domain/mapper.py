from typing import List, Tuple
from .client import Client
from ..domain import entities as E 

class Mapper:
    """ Unitied API to carrier API Mapper (Interface) """
    client: Client

    def create_quote_request(self, payload: E.quote_request):
        """ Create carrier specific quote request xml data from payload """
        raise Exception("Not Supported")

    def parse_quote_response(self, response) -> Tuple[List[E.quote_details], List[E.Error]]:
        """ Create united API quote result list from carrier xml response  """
        raise Exception("Not Supported")

    def create_tracking_request(self, payload: E.tracking_request):
        """ Create carrier specific tracking request xml data from payload """
        raise Exception("Not Supported")

    def parse_tracking_response(self, response) -> Tuple[List[E.tracking_details], List[E.Error]]:
        """ Create united API tracking result list from carrier xml response  """
        raise Exception("Not Supported")

    def create_shipment_request(self, payload: E.shipment_request):
        """ Create carrier specific shipment creation request xml data from payload """
        raise Exception("Not Supported")

    def parse_shipment_response(self, response) -> Tuple[E.shipment_details, List[E.Error]]:
        """ Create united API shipment creation result from carrier xml response  """
        raise Exception("Not Supported")
