from typing import Tuple, List, Union
from functools import reduce
from purplship.mappers.purolator import PurolatorClient
from purplship.domain import Types as T
from pypurolator.EstimatorService import GetFullEstimateRequestContainer
from pypurolator.FreightEstimatingService import GetEstimateRequestContainer
from pypurolator.TrackingService import RequestContainer as TrackingRequestContainer


class PurolatorCapabilities: 
    """
        Purolator native service request types
    """      

    """ Requests """

    def create_estimate_request(self, payload: T.shipment_request) -> GetFullEstimateRequestContainer:
        pass

    def create_freight_estimate_request(self, payload: T.shipment_request) -> GetEstimateRequestContainer:
        pass

    def create_package_tracking_request(self, payload: T.tracking_request) -> TrackingRequestContainer:
        pass    
        

    """ Replys """ 
    
    def parse_estimate_response(self, response: 'XMLElement') -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        pass

    def parse_package_tracking_response(self, response: 'XMLElement') -> Tuple[List[T.TrackingDetails], List[T.Error]]:
        pass


class PurolatorMapperBase(PurolatorCapabilities):
    """
        Purolator mapper base class
    """       
    def __init__(self, client: PurolatorClient):
        self.client = client  

    def parse_error_response(self, response: 'XMLElement') -> List[T.Error]:
        pass

    def _extract_error(self, errors: List[T.Error], messageNode: 'XMLElement') -> List[T.Error]:
        pass
