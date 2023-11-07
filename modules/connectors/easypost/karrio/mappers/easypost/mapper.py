from typing import List, Tuple
from karrio.api.mapper import Mapper as BaseMapper
from karrio.mappers.easypost.settings import Settings
from karrio.core.utils.serializable import Deserializable, Serializable
from karrio.core.models import (
    RateRequest,
    ShipmentRequest,
    ShipmentDetails,
    ShipmentCancelRequest,
    RateDetails,
    Message,
    ConfirmationDetails,
    TrackingDetails,
    TrackingRequest,
)
from karrio.providers.easypost import (
    parse_shipment_cancel_response,
    parse_tracking_response,
    parse_shipment_response,
    parse_rate_response,
    shipment_cancel_request,
    tracking_request,
    shipment_request,
    rate_request,
)


class Mapper(BaseMapper):
    settings: Settings

    # Request Mappers

    def create_rate_request(self, payload: RateRequest) -> Serializable:
        return rate_request(payload, self.settings)

    def create_shipment_request(self, payload: ShipmentRequest) -> Serializable:
        return shipment_request(payload, self.settings)

    def create_cancel_shipment_request(
        self, payload: ShipmentCancelRequest
    ) -> Serializable:
        return shipment_cancel_request(payload, self.settings)

    def create_tracking_request(self, payload: TrackingRequest) -> Serializable:
        return tracking_request(payload, self.settings)

    # Response Parsers

    def parse_rate_response(
        self, response: Deserializable
    ) -> Tuple[List[RateDetails], List[Message]]:
        return parse_rate_response(response, self.settings)

    def parse_shipment_response(
        self, response: Deserializable
    ) -> Tuple[ShipmentDetails, List[Message]]:
        return parse_shipment_response(response, self.settings)

    def parse_cancel_shipment_response(
        self, response: Deserializable
    ) -> Tuple[ConfirmationDetails, List[Message]]:
        return parse_shipment_cancel_response(response, self.settings)

    def parse_tracking_response(
        self, response: Deserializable
    ) -> Tuple[List[TrackingDetails], List[Message]]:
        return parse_tracking_response(response, self.settings)
