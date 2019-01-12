from typing import Tuple, List, Union
from lxml import etree
from purplship.domain.mapper import Mapper
from purplship.domain import Types as T
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

    def create_quote_request(self, payload: T.shipment_request) -> mailing_scenario:
        return self.create_mailing_scenario(payload)

    def create_tracking_request(self, payload: T.tracking_request) -> List[str]:
        return self.create_tracking_pins(payload)

    def create_shipment_request(self, payload: T.shipment_request) -> Union[ShipmentType, NonContractShipmentType]:
        return self.create_shipment(payload)



    def parse_quote_response(self, response: etree.ElementBase) -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        return self.parse_price_quotes(response)

    def parse_tracking_response(self, response: etree.ElementBase) -> Tuple[List[T.TrackingDetails], List[T.Error]]:
        return self.parse_tracking_summary(response)

    def parse_shipment_response(self, response: etree.ElementBase) -> Tuple[T.ShipmentDetails, List[T.Error]]:
        return self.parse_shipment_info(response)