from typing import Tuple, List
from functools import reduce
from purplship.mappers.aramex import AramexClient
from purplship.domain import Types as T
from pyaramex.Rating import RateCalculatorRequest, ClientInfo
from pyaramex.Tracking import ShipmentTrackingRequest


class AramexCapabilities: 
    """
        Aramex native service request types
    """      

    """ Requests """

    def create_rate_calculator_request(self, payload: T.shipment_request) -> RateCalculatorRequest:
        pass

    def create_shipment_tracking_request(self, payload: T.tracking_request) -> ShipmentTrackingRequest:
        pass    
        

    """ Replys """ 
    
    def parse_rate_calculator_response(self, response: 'XMLElement') -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        pass

    def parse_shipment_tracking_response(self, response: 'XMLElement') -> Tuple[List[T.TrackingDetails], List[T.Error]]:
        pass


class AramexMapperBase(AramexCapabilities):
    """
        Aramex mapper base class
    """       
    def __init__(self, client: AramexClient):
        self.client = client
        self.client_info = ClientInfo(
            UserName=self.client.username,
            Password=self.client.password,
            Version=None,
            AccountNumber=self.client.account_number,
            AccountPin=self.client.account_pin,
            AccountEntity=None,
            AccountCountryCode=None
        )

    def parse_error_response(self, response: 'XMLElement') -> List[T.Error]:
        pass

    def _extract_error(self, errors: List[T.Error], messageNode: 'XMLElement') -> List[T.Error]:
        pass
