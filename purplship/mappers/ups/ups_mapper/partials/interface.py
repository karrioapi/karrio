from typing import Tuple, List, Union
from functools import reduce
from purplship.mappers.ups import UPSClient
from purplship.domain import entities as E
from pyups import (
    freight_rate as Rate, 
    package_track as Track, 
    UPSSecurity as Security, 
    error as Err,
    freight_ship as FShip,
    package_ship as PShip
)


class UPSCapabilities: 
    """
        UPS native service request types
    """      

    """ Requests """

    def create_freight_rate_request(self, payload: E.shipment_request) -> Rate.FreightRateRequest:
        pass

    def create_track_request(self, payload: E.tracking_request) -> List[Track.TrackRequest]:
        pass  

    def create_freight_ship_request(self, payload: E.shipment_request) -> FShip.FreightShipRequest:
        pass

    def create_package_ship_request(self, payload: E.shipment_request) -> PShip.ShipmentRequest:
        pass
        

    """ Replys """ 
    
    def parse_freight_rate_response(self, response: 'XMLElement') -> Tuple[List[E.QuoteDetails], List[E.Error]]:
        pass

    def parse_track_response(self, response: 'XMLElement') -> Tuple[List[E.TrackingDetails], List[E.Error]]:
        pass

    def parse_freight_shipment_response(self, response: 'XMLElement') -> Tuple[E.ShipmentDetails, List[E.Error]]:
        pass

    def parse_package_shipment_response(self, response: 'XMLElement') -> Tuple[E.ShipmentDetails, List[E.Error]]:
        pass


class UPSMapperBase(UPSCapabilities):
    """
        UPS mapper base class
    """       
    def __init__(self, client: UPSClient):
        self.client = client

        self.Security = Security.UPSSecurity(
            UsernameToken=Security.UsernameTokenType(
                Username=self.client.username,
                Password=self.client.password
            ),
            ServiceAccessToken=Security.ServiceAccessTokenType(
                AccessLicenseNumber=self.client.access_license_number
            )
        )

    def parse_error_response(self, response) -> List[E.Error]:
        notifications = response.xpath('.//*[local-name() = $name]', name="PrimaryErrorCode")
        return reduce(self._extract_error, notifications, [])

    def _extract_error(self, errors: List[E.Error], errorNode: 'XMLElement') -> List[E.Error]:
        error = Err.CodeType()
        error.build(errorNode)
        return errors + [
            E.Error(code=error.Code, message=error.Description, carrier=self.client.carrier_name)
        ]