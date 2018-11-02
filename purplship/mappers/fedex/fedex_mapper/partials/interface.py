from typing import Tuple, List
from functools import reduce
from purplship.mappers.fedex import FedexClient
from purplship.domain import entities as E
from pyfedex.track_service_v14 import TrackRequest
from pyfedex.ship_service_v21 import ProcessShipmentRequest
from pyfedex.rate_v22 import (
    RateRequest, 
    WebAuthenticationCredential, 
    WebAuthenticationDetail, 
    ClientDetail, 
    Notification
)


class FedexCapabilities: 
    """
        FedEx native service request types
    """      

    """ Requests """ 

    def create_rate_request(self, payload: E.shipment_request) -> RateRequest:
        pass

    def create_track_request(self, payload: E.tracking_request) -> TrackRequest:
        pass

    def create_process_shipment_request(self, payload: E.shipment_request) -> ProcessShipmentRequest:
        pass    
        

    """ Replys """ 
    
    def parse_rate_reply(self, response: 'XMLElement') -> Tuple[List[E.QuoteDetails], List[E.Error]]:
        pass

    def parse_track_reply(self, response: 'XMLElement') -> Tuple[List[E.TrackingDetails], List[E.Error]]:
        pass

    def parse_process_shipment_reply(self, response: 'XMLElement') -> Tuple[E.ShipmentDetails, List[E.Error]]:
        pass


class FedexMapperBase(FedexCapabilities):
    """
        FedEx mapper base class
    """       
    def __init__(self, client: FedexClient):
        self.client = client

        userCredential = WebAuthenticationCredential(Key=client.user_key, Password=client.password)
        self.webAuthenticationDetail = WebAuthenticationDetail(UserCredential=userCredential)
        self.clientDetail = ClientDetail(AccountNumber=client.account_number, MeterNumber=client.meter_number)    

    def parse_error_response(self, response: 'XMLElement') -> List[E.Error]:
        notifications = response.xpath(
            './/*[local-name() = $name]', name="Notifications"
        ) + response.xpath(
            './/*[local-name() = $name]', name="Notification"
        )
        return reduce(self._extract_error, notifications, [])

    def _extract_error(self, errors: List[E.Error], notificationNode: 'XMLElement') -> List[E.Error]:
        notification = Notification()
        notification.build(notificationNode)
        if notification.Severity in ('SUCCESS', 'NOTE'):
            return errors
        return errors + [
            E.Error(code=notification.Code, message=notification.Message, carrier=self.client.carrier_name)
        ]
