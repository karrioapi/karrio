from typing import Tuple, List
from functools import reduce
from purplship.mappers.usps import USPSClient
from purplship.domain import entities as E
from pyusps.ratev4request import RateV4Request
from pyusps.intlratev2request import IntlRateV2Request
from pyusps.trackrequest import TrackRequest


class USPSCapabilities: 
    """
        USPS native service request types
    """      

    """ Requests """

    def create_rate_request(self, payload: E.shipment_request) -> RateV4Request:
        pass

    def create_intl_rate_request(self, payload: E.shipment_request) -> IntlRateV2Request:
        pass

    def create_track_request(self, payload: E.tracking_request) -> TrackRequest:
        pass    
        

    """ Replys """ 
    
    def parse_rate_response(self, response: 'XMLElement') -> Tuple[List[E.QuoteDetails], List[E.Error]]:
        pass

    def parse_track_response(self, response: 'XMLElement') -> Tuple[List[E.TrackingDetails], List[E.Error]]:
        pass


class USPSMapperBase(USPSCapabilities):
    """
        USPS mapper base class
    """       
    def __init__(self, client: USPSClient):
        self.client = client  

    def parse_error_response(self, response: 'XMLElement') -> List[E.Error]:
        pass

    def _extract_error(self, errors: List[E.Error], messageNode: 'XMLElement') -> List[E.Error]:
        pass
