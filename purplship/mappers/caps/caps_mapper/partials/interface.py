from typing import Tuple, List, Union
from functools import reduce
from purplship.mappers.caps import CanadaPostClient
from purplship.domain import entities as E
from pycaps.rating import mailing_scenario
from pycaps.shipment import ShipmentType
from pycaps.ncshipment import NonContractShipmentType
from pycaps.messages import messageType


class CanadaPostCapabilities: 
    """
        CanadaPost native service request types
    """      

    """ Requests """

    def create_mailing_scenario(self, payload: E.shipment_request) -> mailing_scenario:
        pass

    def create_tracking_pins(self, payload: E.tracking_request) -> List[str]:
        pass

    def create_shipment(self, payload: E.shipment_request) -> Union[ShipmentType, NonContractShipmentType]:
        pass    
        

    """ Replys """ 
    
    def parse_price_quotes(self, response: 'XMLElement') -> Tuple[List[E.QuoteDetails], List[E.Error]]:
        pass

    def parse_tracking_summary(self, response: 'XMLElement') -> Tuple[List[E.TrackingDetails], List[E.Error]]:
        pass

    def parse_shipment_info(self, response: 'XMLElement') -> Tuple[E.ShipmentDetails, List[E.Error]]:
        pass


class CanadaPostMapperBase(CanadaPostCapabilities):
    """
        CanadaPost mapper base class
    """       
    def __init__(self, client: CanadaPostClient):
        self.client = client  

    def parse_error_response(self, response: 'XMLElement') -> List[E.Error]:
        messages = response.xpath('.//*[local-name() = $name]', name="message")
        return reduce(self._extract_error, messages, [])

    def _extract_error(self, errors: List[E.Error], messageNode: 'XMLElement') -> List[E.Error]:
        message = messageType()
        message.build(messageNode)
        return errors + [
            E.Error(code=message.code,
                    message=message.description, carrier=self.client.carrier_name)
        ]
