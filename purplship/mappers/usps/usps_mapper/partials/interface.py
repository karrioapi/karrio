from typing import Tuple, List
from functools import reduce
from purplship.mappers.usps import USPSClient
from purplship.domain import Types as T
from pyusps.RateV4Request import RateV4Request
from pyusps.IntlRateV2Request import IntlRateV2Request
from pyusps.TrackRequest import TrackRequest


class USPSCapabilities: 
    """
        USPS native service request types
    """      

    """ Requests """

    def create_rate_request(self, payload: T.shipment_request) -> RateV4Request:
        pass

    def create_intl_rate_request(self, payload: T.shipment_request) -> IntlRateV2Request:
        pass

    def create_track_request(self, payload: T.tracking_request) -> TrackRequest:
        pass    
        

    """ Replys """ 
    
    def parse_rate_response(self, response: 'XMLElement') -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        pass

    def parse_track_response(self, response: 'XMLElement') -> Tuple[List[T.TrackingDetails], List[T.Error]]:
        pass


class USPSMapperBase(USPSCapabilities):
    """
        USPS mapper base class
    """       
    def __init__(self, client: USPSClient):
        self.client = client  

    def parse_error_response(self, response: 'XMLElement') -> List[T.Error]:
        pass

    def _extract_error(self, errors: List[T.Error], messageNode: 'XMLElement') -> List[T.Error]:
        pass
