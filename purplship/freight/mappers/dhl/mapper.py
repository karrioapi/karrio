from typing import List
from pydhl.DCT_req_global import DCTRequest
from pydhl.ship_val_global_req_61 import ShipmentRequest as DHLShipmentRequest
from pydhl.tracking_request_known import KnownTrackingRequest
from pydhl.book_pickup_global_req_20 import BookPURequest
from pydhl.modify_pickup_global_req_20 import ModifyPURequest
from pydhl.cancel_pickup_global_req_20 import CancelPURequest
from purplship.freight.mapper import Mapper as BaseMapper
from purplship.core.utils.serializable import Serializable, Deserializable
from purplship.core.models import (
    RateRequest, RateDetails, TrackingRequest, TrackingDetails,
    ShipmentRequest, ShipmentDetails, PickupRequest, PickupDetails,
    PickupUpdateRequest, PickupCancellationRequest, Error
)
from purplship.carriers.dhl import (
    dct_request, parse_dct_response,
    known_tracking_request, parse_known_tracking_response,
    shipment_request, parse_shipment_response,
    book_pickup_request, parse_book_pickup_response,
    cancel_pickup_request, parse_cancel_pickup_response,
    modify_pickup_request, parse_modify_pickup_response
)
from purplship.freight.mappers.dhl.settings import Settings


class Mapper(BaseMapper):
    settings: Settings

    def create_rate_request(self, payload: RateRequest) -> Serializable[DCTRequest]:
        return dct_request(payload, self.settings)

    def create_tracking_request(self, payload: TrackingRequest) -> Serializable[KnownTrackingRequest]:
        return known_tracking_request(payload, self.settings)

    def create_shipment_request(self, payload: ShipmentRequest) -> Serializable[DHLShipmentRequest]:
        return shipment_request(payload, self.settings)

    def create_pickup_request(self, payload: PickupRequest) -> Serializable[BookPURequest]:
        return book_pickup_request(payload, self.settings)

    def create_modify_pickup_request(self, payload: PickupUpdateRequest) -> Serializable[ModifyPURequest]:
        return modify_pickup_request(payload, self.settings)

    def create_cancel_pickup_request(self, payload: PickupCancellationRequest) -> Serializable[CancelPURequest]:
        return cancel_pickup_request(payload, self.settings)

    def parse_rate_response(self, response: Deserializable[str]) -> (List[RateDetails], List[Error]):
        return parse_dct_response(response.deserialize(), self.settings)

    def parse_tracking_response(self, response: Deserializable[str]) -> (List[TrackingDetails], List[Error]):
        return parse_known_tracking_response(response.deserialize(), self.settings)

    def parse_shipment_response(self, response: Deserializable[str]) -> (ShipmentDetails, List[Error]):
        return parse_shipment_response(response.deserialize(), self.settings)

    def parse_pickup_response(self, response: Deserializable[str]) -> (PickupDetails, List[Error]):
        return parse_book_pickup_response(response.deserialize(), self.settings)

    def parse_modify_pickup_response(self, response: Deserializable[str]) -> (PickupDetails, List[Error]):
        return parse_modify_pickup_response(response.deserialize(), self.settings)

    def parse_cancel_pickup_response(self, response: Deserializable[str]) -> (dict, List[Error]):
        return parse_cancel_pickup_response(response.deserialize(), self.settings)
