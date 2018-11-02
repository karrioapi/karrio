from typing import List, Tuple
from .client import Client
from ..domain import entities as E 

class Mapper:
    """ Unitied API to carrier API Mapper (Interface) """
    client: Client

    def create_quote_request(self, payload: E.shipment_request):
        """ Create carrier specific quote request xml data from payload """
        raise Exception("Not Supported")

    def parse_quote_response(self, response) -> Tuple[List[E.QuoteDetails], List[E.Error]]:
        """ Create united API quote result list from carrier xml response  """
        raise Exception("Not Supported")

    def create_tracking_request(self, payload: E.tracking_request):
        """ Create carrier specific tracking request xml data from payload """
        raise Exception("Not Supported")

    def parse_tracking_response(self, response) -> Tuple[List[E.TrackingDetails], List[E.Error]]:
        """ Create united API tracking result list from carrier xml response  """
        raise Exception("Not Supported")

    def create_shipment_request(self, payload: E.shipment_request):
        """ Create carrier specific shipment creation request xml data from payload """
        raise Exception("Not Supported")

    def parse_shipment_response(self, response) -> Tuple[E.ShipmentDetails, List[E.Error]]:
        """ Create united API shipment creation result from carrier xml response  """
        raise Exception("Not Supported")

    def create_pickup_request(self, payload: E.pickup_request):
        """ Create carrier specific pickup request xml data from payload """
        raise Exception("Not Supported")

    def modify_pickup_request(self, payload: E.pickup_request):
        """ Create carrier specific pickup modification request xml data from payload """
        raise Exception("Not Supported")

    def parse_pickup_response(self, response) -> Tuple[E.PickupDetails, List[E.Error]]:
        """ Create united API pickup result from carrier xml response  """
        raise Exception("Not Supported")

    def create_pickup_cancellation_request(self, payload: E.pickup_cancellation_request):
        """ Create carrier specific pickup cancellation request xml data from payload """
        raise Exception("Not Supported")

    def parse_pickup_cancellation_response(self, response) -> Tuple[dict, List[E.Error]]:
        """ Create united API pickup cancellation result from carrier xml response  """
        raise Exception("Not Supported")