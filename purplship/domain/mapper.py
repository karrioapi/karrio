"""PurplShip Mapper base class definition module."""

from abc import ABC
from typing import List, Tuple
from ..domain import Types as T


class Mapper(ABC):
    """ 
    United API to carrier data Mapper (Interface) 
    ...

    Attributes
    ----------
    client : Client
            a carrier client (holding connection settings)
    """

    def create_quote_request(self, payload: T.RateRequest):
        """ Create a carrier specific quote request data from payload """
        raise Exception("Not Supported")

    def parse_quote_response(
        self, response
    ) -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        """ Create a united API quote result list from carrier response  """
        raise Exception("Not Supported")

    def create_tracking_request(self, payload: T.TrackingRequest):
        """ Create a carrier specific tracking request data from payload """
        raise Exception("Not Supported")

    def parse_tracking_response(
        self, response
    ) -> Tuple[List[T.TrackingDetails], List[T.Error]]:
        """ Create a united API tracking result list from carrier response  """
        raise Exception("Not Supported")

    def create_shipment_request(self, payload: T.ShipmentRequest):
        """ Create a carrier specific shipment creation request data from payload """
        raise Exception("Not Supported")

    def parse_shipment_response(
        self, response
    ) -> Tuple[T.ShipmentDetails, List[T.Error]]:
        """ Create a united API shipment creation result from carrier response  """
        raise Exception("Not Supported")

    def create_pickup_request(self, payload: T.PickupRequest):
        """ Create a carrier specific pickup request xml data from payload """
        raise Exception("Not Supported")

    def modify_pickup_request(self, payload: T.PickupRequest):
        """ Create a carrier specific pickup modification request data from payload """
        raise Exception("Not Supported")

    def parse_pickup_response(self, response) -> Tuple[T.PickupDetails, List[T.Error]]:
        """ Create a united API pickup result from carrier response  """
        raise Exception("Not Supported")

    def create_pickup_cancellation_request(
        self, payload: T.PickupCancellationRequest
    ):
        """ Create a carrier specific pickup cancellation request data from payload """
        raise Exception("Not Supported")

    def parse_pickup_cancellation_response(
        self, response
    ) -> Tuple[dict, List[T.Error]]:
        """ Create a united API pickup cancellation result from carrier response  """
        raise Exception("Not Supported")
