from typing import List, Tuple
from purplship.core.utils.serializable import Serializable, Deserializable
from purplship.api.mapper import Mapper as BaseMapper
from purplship.core.models import (
    ShipmentRequest,
    TrackingRequest,
    Message,
    TrackingDetails,
    RateDetails,
    RateRequest,
    ShipmentDetails,
    AddressValidationRequest,
    AddressValidationDetails,
    PickupRequest,
    PickupUpdateRequest,
    PickupDetails,
    PickupCancelRequest,
    ConfirmationDetails,
    ShipmentCancelRequest
)
from purplship.core.utils import Envelope, Pipeline
from purplship.providers.canpar import (
    rate_shipment_request,
    parse_rate_shipment_response,
    track_by_barcode,
    parse_track_response,
    create_shipment_pipeline,
    parse_shipment_response,
    void_shipment_request,
    parse_void_shipment_response,
    cancel_pickup_request,
    parse_cancel_pickup_response,
    schedule_pickup_request,
    parse_schedule_pickup_response,
    update_pickup_request,
    search_canada_post,
    parse_search_response,
)
from purplship.mappers.canpar.settings import Settings


class Mapper(BaseMapper):
    settings: Settings

    """Request Mappers"""

    def create_address_validation_request(self, payload: AddressValidationRequest) -> Serializable[Envelope]:
        return search_canada_post(payload, self.settings)

    def create_rate_request(
        self, payload: RateRequest
    ) -> Serializable[Envelope]:
        return rate_shipment_request(payload, self.settings)

    def create_tracking_request(
        self, payload: TrackingRequest
    ) -> Serializable[Envelope]:
        return track_by_barcode(payload, self.settings)

    def create_shipment_request(
        self, payload: ShipmentRequest
    ) -> Serializable[Pipeline]:
        return create_shipment_pipeline(payload, self.settings)

    def create_cancel_shipment_request(self, payload: ShipmentCancelRequest) -> Serializable:
        return void_shipment_request(payload, self.settings)

    def create_pickup_request(self, payload: PickupRequest) -> Serializable[Envelope]:
        return schedule_pickup_request(payload, self.settings)

    def create_pickup_update_request(
        self, payload: PickupUpdateRequest
    ) -> Serializable[Pipeline]:
        return update_pickup_request(payload, self.settings)

    def create_cancel_pickup_request(
        self, payload: PickupCancelRequest
    ) -> Serializable[Envelope]:
        return cancel_pickup_request(payload, self.settings)

    """Response Parsers"""

    def parse_address_validation_response(
        self, response: Deserializable[str]
    ) -> Tuple[AddressValidationDetails, List[Message]]:
        return parse_search_response(response.deserialize(), self.settings)

    def parse_rate_response(
        self, response: Deserializable[str]
    ) -> Tuple[List[RateDetails], List[Message]]:
        return parse_rate_shipment_response(response.deserialize(), self.settings)

    def parse_tracking_response(
        self, response: Deserializable[str]
    ) -> Tuple[List[TrackingDetails], List[Message]]:
        return parse_track_response(response.deserialize(), self.settings)

    def parse_shipment_response(
        self, response: Deserializable[str]
    ) -> Tuple[ShipmentDetails, List[Message]]:
        return parse_shipment_response(response.deserialize(), self.settings)

    def parse_cancel_shipment_response(
        self, response: Deserializable[str]
    ) -> Tuple[ConfirmationDetails, List[Message]]:
        return parse_void_shipment_response(response.deserialize(), self.settings)

    def parse_pickup_response(
        self, response: Deserializable[str]
    ) -> Tuple[PickupDetails, List[Message]]:
        return parse_schedule_pickup_response(response.deserialize(), self.settings)

    def parse_pickup_update_response(
        self, response: Deserializable[str]
    ) -> Tuple[PickupDetails, List[Message]]:
        return parse_schedule_pickup_response(response.deserialize(), self.settings)

    def parse_cancel_pickup_response(
        self, response: Deserializable[str]
    ) -> Tuple[ConfirmationDetails, List[Message]]:
        return parse_cancel_pickup_response(response.deserialize(), self.settings)
