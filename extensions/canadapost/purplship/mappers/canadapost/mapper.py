from typing import List, Tuple
from pycanadapost.rating import mailing_scenario
from pycanadapost.pickuprequest import (
    PickupRequestDetailsType,
    PickupRequestResponseDetailsType,
)
from purplship.core.utils.pipeline import Pipeline
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
    PickupRequest,
    PickupDetails,
    PickupUpdateRequest,
    PickupCancellationRequest,
    ConfirmationDetails,
)
from purplship.providers.canadapost import (
    mailing_scenario_request,
    parse_price_quotes,
    tracking_pins_request,
    parse_tracking_summary,
    shipment_request,
    parse_shipment_response,
    cancel_pickup_request,
    create_pickup_request,
    update_pickup_request,
    parse_pickup_response,
    parse_cancel_pickup_response,
)
from purplship.mappers.canadapost.settings import Settings


class Mapper(BaseMapper):
    settings: Settings

    """Request Mappers"""

    def create_rate_request(
        self, payload: RateRequest
    ) -> Serializable[mailing_scenario]:
        return mailing_scenario_request(payload, self.settings)

    def create_tracking_request(
        self, payload: TrackingRequest
    ) -> Serializable[List[str]]:
        return tracking_pins_request(payload)

    def create_shipment_request(
        self, payload: ShipmentRequest
    ) -> Serializable[Pipeline]:
        return shipment_request(payload, self.settings)

    def create_pickup_request(
        self, payload: PickupRequest
    ) -> Serializable[PickupRequestDetailsType]:
        return create_pickup_request(payload, self.settings)

    def create_modify_pickup_request(
        self, payload: PickupUpdateRequest
    ) -> Serializable[PickupRequestResponseDetailsType]:
        return update_pickup_request(payload, self.settings)

    def create_cancel_pickup_request(
        self, payload: PickupCancellationRequest
    ) -> Serializable[str]:
        return cancel_pickup_request(payload, self.settings)

    """Response Parsers"""

    def parse_rate_response(
        self, response: Deserializable[str]
    ) -> Tuple[List[RateDetails], List[Message]]:
        return parse_price_quotes(response.deserialize(), self.settings)

    def parse_tracking_response(
        self, response: Deserializable[str]
    ) -> Tuple[List[TrackingDetails], List[Message]]:
        return parse_tracking_summary(response.deserialize(), self.settings)

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
        return parse_cancel_pickup_response(response.deserialize(), self.settings)
