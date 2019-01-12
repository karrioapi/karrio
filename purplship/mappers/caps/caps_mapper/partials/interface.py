from typing import Tuple, List, Union
from functools import reduce
from lxml import etree
from purplship.mappers.caps import CanadaPostClient
from purplship.domain import Types as T
from pycaps.rating import mailing_scenario
from pycaps.shipment import ShipmentType
from pycaps.ncshipment import NonContractShipmentType
from pycaps.messages import messageType


class CanadaPostCapabilities: 
    """
        CanadaPost native service request types
    """      

    """ Requests """

    def create_mailing_scenario(self, payload: T.shipment_request) -> mailing_scenario:
        pass

    def create_tracking_pins(self, payload: T.tracking_request) -> List[str]:
        pass

    def create_shipment(self, payload: T.shipment_request) -> Union[ShipmentType, NonContractShipmentType]:
        pass    
        

    """ Replys """ 
    
    def parse_price_quotes(self, response: etree.ElementBase) -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        pass

    def parse_tracking_summary(self, response: etree.ElementBase) -> Tuple[List[T.TrackingDetails], List[T.Error]]:
        pass

    def parse_shipment_info(self, response: etree.ElementBase) -> Tuple[T.ShipmentDetails, List[T.Error]]:
        pass


class CanadaPostMapperBase(CanadaPostCapabilities):
    """
        CanadaPost mapper base class
    """  
    def __init__(self, client: CanadaPostClient):
        self.client : CanadaPostClient = client  

    def parse_error_response(self, response: etree.ElementBase) -> List[T.Error]:
        messages = response.xpath('.//*[local-name() = $name]', name="message")
        return reduce(self._extract_error, messages, [])

    def _extract_error(self, errors: List[T.Error], messageNode: etree.ElementBase) -> List[T.Error]:
        message = messageType()
        message.build(messageNode)
        return errors + [
            T.Error(code=message.code,
                    message=message.description, carrier=self.client.carrier_name)
        ]
