from typing import List, Tuple
from pyfedex.track_service_v18 import TrackRequest
from pyfedex.ship_service_v25 import ProcessShipmentRequest
from pyfedex.rate_service_v26 import RateRequest as FedexRateRequest
from pyfedex.pickup_service_v20 import CancelPickupRequest
from purplship.core.utils import Serializable, Deserializable, Pipeline
from purplship.core.models import (
    RateDetails,
    RateRequest,
    TrackingDetails,
    TrackingRequest,
    ShipmentRequest,
    ShipmentDetails,
    Message,
    PickupDetails,
    PickupRequest,
    PickupUpdateRequest,
    PickupCancellationRequest,
    ConfirmationDetails,
)
from purplship.providers.fedex import track_request, parse_track_response
from purplship.providers.fedex.pickup import (
    create_pickup_request,
    update_pickup_request,
    cancel_pickup_request,
    parse_pickup_response,
    parse_cancel_pickup_reply,
)
from purplship.providers.fedex.package import (
    rate_request,
    parse_rate_response,
    process_shipment_request,
    parse_shipment_response,
)
from purplship.mappers.fedex_express.settings import Settings
from purplship.api.mapper import Mapper as BaseMapper


class Mapper(BaseMapper):
    settings: Settings

    """Request Mappers"""

    def create_rate_request(
        self, payload: RateRequest
    ) -> Serializable[FedexRateRequest]:
        return rate_request(payload, self.settings)

    def create_tracking_request(
        self, payload: TrackingRequest
    ) -> Serializable[TrackRequest]:
        return track_request(payload, self.settings)

    def create_shipment_request(
        self, payload: ShipmentRequest
    ) -> Serializable[ProcessShipmentRequest]:
        return process_shipment_request(payload, self.settings)

    def create_pickup_request(self, payload: PickupRequest) -> Serializable[Pipeline]:
        return create_pickup_request(payload, self.settings)

    def create_modify_pickup_request(
        self, payload: PickupUpdateRequest
    ) -> Serializable[Pipeline]:
        return update_pickup_request(payload, self.settings)

    def create_cancel_pickup_request(
        self, payload: PickupCancellationRequest
    ) -> Serializable[CancelPickupRequest]:
        return cancel_pickup_request(payload, self.settings)

    """Response Parsers"""

    def parse_rate_response(
        self, response: Deserializable[str]
    ) -> Tuple[List[RateDetails], List[Message]]:
        return parse_rate_response(response.deserialize(), self.settings)

    def parse_tracking_response(
        self, response: Deserializable[str]
    ) -> Tuple[List[TrackingDetails], List[Message]]:
        return parse_track_response(response.deserialize(), self.settings)

    def parse_shipment_response(
        self, response: Deserializable[str]
    ) -> Tuple[ShipmentDetails, List[Message]]:
        return parse_shipment_response(response.deserialize(), self.settings)

    def parse_pickup_response(
        self, response: Deserializable[str]
    ) -> Tuple[PickupDetails, List[Message]]:
        return parse_pickup_response(response.deserialize(), self.settings)

    def parse_modify_pickup_response(
        self, response: Deserializable[str]
    ) -> Tuple[PickupDetails, List[Message]]:
        return parse_pickup_response(response.deserialize(), self.settings)

    def parse_cancel_pickup_response(
        self, response: Deserializable[str]
    ) -> Tuple[ConfirmationDetails, List[Message]]:
        return parse_cancel_pickup_reply(response.deserialize(), self.settings)
