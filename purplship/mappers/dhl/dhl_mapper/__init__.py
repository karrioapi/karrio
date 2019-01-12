from typing import Tuple, List, Union
from lxml import etree
from purplship.domain.mapper import Mapper
from purplship.domain import Types as T
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

    def create_quote_request(self, payload: T.shipment_request) -> Req.DCTRequest:
        return self.create_dct_request(payload)

    def create_tracking_request(self, payload: T.tracking_request) -> Track.KnownTrackingRequest:
        return self.create_dhltracking_request(payload)

    def create_shipment_request(self, payload: T.shipment_request) -> ShipReq.ShipmentRequest:
        return self.create_dhlshipment_request(payload)

    def create_pickup_request(self, payload: T.pickup_request) -> BookPUReq.BookPURequest:
        return self.create_book_purequest(payload)

    def modify_pickup_request(self, payload: T.pickup_request) -> ModifPUReq.ModifyPURequest:
        return self.create_modify_purequest(payload)

    def create_pickup_cancellation_request(self, payload: T.pickup_cancellation_request) -> CancelPUReq.CancelPURequest:
        return self.create_cancel_purequest(payload)


    def parse_quote_response(self, response: etree.ElementBase) -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        return self.parse_dct_response(response)

    def parse_tracking_response(self, response: etree.ElementBase) -> Tuple[List[T.TrackingDetails], List[T.Error]]:
        return self.parse_dhltracking_response(response)

    def parse_shipment_response(self, response: etree.ElementBase) -> Tuple[T.ShipmentDetails, List[T.Error]]:
        return self.parse_dhlshipment_respone(response)

    def parse_pickup_response(self, response) -> Tuple[T.PickupDetails, List[T.Error]]:
        return self.parse_book_puresponse(response)

    def parse_pickup_cancellation_response(self, response) -> Tuple[dict, List[T.Error]]:
        return self.parse_cancel_puresponse(response)