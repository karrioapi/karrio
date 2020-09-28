from typing import List, Tuple
from purplship.api.mapper import Mapper as BaseMapper
from purplship.mappers.purolator_courier.settings import Settings
from purplship.core.utils import Deserializable, Serializable, Pipeline
from purplship.core.utils.soap import Envelope
from purplship.core.models import (
    RateRequest,
    ShipmentRequest,
    TrackingRequest,
    ShipmentDetails,
    RateDetails,
    TrackingDetails,
    Message,
    PickupRequest,
    PickupUpdateRequest,
    PickupDetails,
    ConfirmationDetails,
    PickupCancellationRequest,
)
from purplship.providers.purolator.package import (
    parse_track_package_response,
    track_package_by_pin_request,
    parse_full_estimate_response,
    get_full_estimate_request,
    parse_shipment_creation_response,
    create_shipment_request,
    void_pickup_request,
    parse_void_pickup_reply,
    schedule_pickup_pipeline,
    parse_schedule_pickup_reply,
    modify_pickup_pipeline,
    parse_modify_pickup_reply,
)


class Mapper(BaseMapper):
    settings: Settings

    """Request Mappers"""

    def create_rate_request(self, payload: RateRequest) -> Serializable[Envelope]:
        return get_full_estimate_request(payload, self.settings)

    def create_tracking_request(
        self, payload: TrackingRequest
    ) -> Serializable[Envelope]:
        return track_package_by_pin_request(payload, self.settings)

    def create_shipment_request(
        self, payload: ShipmentRequest
    ) -> Serializable[Pipeline]:
        return create_shipment_request(payload, self.settings)

    def create_pickup_request(self, payload: PickupRequest) -> Serializable[Pipeline]:
        return schedule_pickup_pipeline(payload, self.settings)

    def create_modify_pickup_request(
        self, payload: PickupUpdateRequest
    ) -> Serializable[Pipeline]:
        return modify_pickup_pipeline(payload, self.settings)

    def create_cancel_pickup_request(
        self, payload: PickupCancellationRequest
    ) -> Serializable[Envelope]:
        return void_pickup_request(payload, self.settings)

    """Response Parsers"""

    def parse_rate_response(
        self, response: Deserializable[str]
    ) -> Tuple[List[RateDetails], List[Message]]:
        return parse_full_estimate_response(response.deserialize(), self.settings)

    def parse_tracking_response(
        self, response: Deserializable[str]
    ) -> Tuple[List[TrackingDetails], List[Message]]:
        return parse_track_package_response(response.deserialize(), self.settings)

    def parse_shipment_response(
        self, response: Deserializable[str]
    ) -> Tuple[ShipmentDetails, List[Message]]:
        return parse_shipment_creation_response(response.deserialize(), self.settings)

    def parse_pickup_response(
        self, response: Deserializable[str]
    ) -> Tuple[PickupDetails, List[Message]]:
        return parse_schedule_pickup_reply(response.deserialize(), self.settings)

    def parse_modify_pickup_response(
        self, response: Deserializable[str]
    ) -> Tuple[PickupDetails, List[Message]]:
        return parse_modify_pickup_reply(response.deserialize(), self.settings)

    def parse_cancel_pickup_response(
        self, response: Deserializable
    ) -> Tuple[ConfirmationDetails, List[Message]]:
        return parse_void_pickup_reply(response.deserialize(), self.settings)
