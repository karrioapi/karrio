from typing import Tuple, List, Union
from purplship.domain.mapper import Mapper
from purplship.domain import entities as E
from pycaps.rating import mailing_scenario
from pycaps.shipment import ShipmentType
from pycaps.ncshipment import NonContractShipmentType
from .partials import (
    CanadaPostRateMapperPartial, 
    CanadaPostTrackMapperPartial, 
    CanadaPostShipmentMapperPartial
)


class CanadaPostMapper(
        Mapper,
        CanadaPostRateMapperPartial,
        CanadaPostTrackMapperPartial,
        CanadaPostShipmentMapperPartial
    ):        

    def create_quote_request(self, payload: E.shipment_request) -> mailing_scenario:
        return self.create_mailing_scenario(payload)

    def create_tracking_request(self, payload: E.tracking_request) -> List[str]:
        return self.create_tracking_pins(payload)

    def create_shipment_request(self, payload: E.shipment_request) -> Union[ShipmentType, NonContractShipmentType]:
        return self.create_shipment(payload)



    def parse_quote_response(self, response: 'XMLElement') -> Tuple[List[E.QuoteDetails], List[E.Error]]:
        return self.parse_price_quotes(response)

    def parse_tracking_response(self, response: 'XMLElement') -> Tuple[List[E.TrackingDetails], List[E.Error]]:
        return self.parse_tracking_summary(response)

    def parse_shipment_response(self, response: 'XMLElement') -> Tuple[E.ShipmentDetails, List[E.Error]]:
        return self.parse_shipment_info(response)