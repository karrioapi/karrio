from typing import Tuple, List, Union
from purplship.domain.mapper import Mapper
from purplship.domain import entities as E
from pydhl import (
    DCT_req_global as Req,
    ship_val_global_req_61 as ShipReq,
    DCT_Response_global as Res,
    tracking_request_known as Track,
    tracking_response as TrackRes,
    book_pickup_global_req_20 as BookPUReq,
    modify_pickup_global_req_20 as ModifPUReq,
    cancel_pickup_global_req_20 as CancelPUReq
)
from .partials import (
    DHLQuoteMapperPartial, 
    DHLTrackMapperPartial, 
    DHLShipmentMapperPartial,
    DHLPickupMapperPartial
)


class DHLMapper(
        Mapper,
        DHLQuoteMapperPartial,
        DHLTrackMapperPartial,
        DHLShipmentMapperPartial,
        DHLPickupMapperPartial
    ):        

    def create_quote_request(self, payload: E.shipment_request) -> Req.DCTRequest:
        return self.create_dct_request(payload)

    def create_tracking_request(self, payload: E.tracking_request) -> Track.KnownTrackingRequest:
        return self.create_dhltracking_request(payload)

    def create_shipment_request(self, payload: E.shipment_request) -> ShipReq.ShipmentRequest:
        return self.create_dhlshipment_request(payload)

    def create_pickup_request(self, payload: E.pickup_request) -> BookPUReq.BookPURequest:
        return self.create_book_purequest(payload)

    def modify_pickup_request(self, payload: E.pickup_request) -> ModifPUReq.ModifyPURequest:
        return self.create_modify_purequest(payload)

    def create_pickup_cancellation_request(self, payload: E.pickup_cancellation_request) -> CancelPUReq.CancelPURequest:
        return self.create_cancel_purequest(payload)


    def parse_quote_response(self, response: 'XMLElement') -> Tuple[List[E.QuoteDetails], List[E.Error]]:
        return self.parse_dct_response(response)

    def parse_tracking_response(self, response: 'XMLElement') -> Tuple[List[E.TrackingDetails], List[E.Error]]:
        return self.parse_dhltracking_response(response)

    def parse_shipment_response(self, response: 'XMLElement') -> Tuple[E.ShipmentDetails, List[E.Error]]:
        return self.parse_dhlshipment_respone(response)

    def parse_pickup_response(self, response) -> Tuple[E.PickupDetails, List[E.Error]]:
        return self.parse_book_puresponse(response)

    def parse_pickup_cancellation_response(self, response) -> Tuple[dict, List[E.Error]]:
        return self.parse_cancel_puresponse(response)