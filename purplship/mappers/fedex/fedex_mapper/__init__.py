from typing import Tuple, List
from lxml import etree
from purplship.domain.mapper import Mapper
from purplship.domain import Types as T
from pyfedex.track_service_v14 import TrackRequest
from pyfedex.ship_service_v21 import ProcessShipmentRequest
from pyfedex.rate_v22 import (
    RateRequest, 
    WebAuthenticationCredential, 
    WebAuthenticationDetail, 
    ClientDetail, 
    Notification
)
from .partials import (
    FedexRateMapperPartial, 
    FedexTrackMapperPartial, 
    FedexShipmentMapperPartial
)


class FedexMapper(
        Mapper,
        FedexRateMapperPartial,
        FedexTrackMapperPartial,
        FedexShipmentMapperPartial
    ):        

    def create_quote_request(self, payload: T.shipment_request) -> RateRequest:
        return self.create_rate_request(payload)

    def create_tracking_request(self, payload: T.tracking_request) -> TrackRequest:
        return self.create_track_request(payload)

    def create_shipment_request(self, payload: T.shipment_request) -> ProcessShipmentRequest:
        return self.create_process_shipment_request(payload)


    def parse_quote_response(self, response: etree.ElementBase) -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        return self.parse_rate_reply(response)

    def parse_tracking_response(self, response: etree.ElementBase) -> Tuple[List[T.TrackingDetails], List[T.Error]]:
        return self.parse_track_reply(response)

    def parse_shipment_response(self, response: etree.ElementBase) -> Tuple[T.ShipmentDetails, List[T.Error]]:
        return self.parse_process_shipment_reply(response)