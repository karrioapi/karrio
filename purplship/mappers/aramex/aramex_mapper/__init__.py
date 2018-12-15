from typing import Tuple, List, Union
from purplship.domain.mapper import Mapper
from purplship.domain import Types as T
from pyaramex.Rating import RateCalculatorRequest
from pyaramex.Tracking import ShipmentTrackingRequest
from .partials import (
    AramexRateMapperPartial, 
    AramexTrackMapperPartial
)


class AramexMapper(
        Mapper,
        AramexRateMapperPartial,
        AramexTrackMapperPartial
    ):        

    def create_quote_request(self, payload: T.shipment_request) -> RateCalculatorRequest:
        return self.create_rate_calculator_request(payload)

    def create_tracking_request(self, payload: T.tracking_request) -> ShipmentTrackingRequest:
        return self.create_shipment_tracking_request(payload)



    def parse_quote_response(self, response: 'XMLElement') -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        return self.parse_rate_calculator_response(response)

    def parse_tracking_response(self, response: 'XMLElement') -> Tuple[List[T.TrackingDetails], List[T.Error]]:
        return self.parse_shipment_tracking_response(response)