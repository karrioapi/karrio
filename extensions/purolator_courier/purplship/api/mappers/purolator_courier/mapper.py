from typing import List, Tuple
from purplship.api.mapper import Mapper as BaseMapper
from purplship.api.mappers.purolator_courier.settings import Settings
from purplship.core.utils.serializable import Deserializable, Serializable
from purplship.core.utils.xml import Element
from purplship.core.models import (
    RateRequest,
    ShipmentRequest,
    TrackingRequest,
    ShipmentDetails,
    RateDetails,
    TrackingDetails,
    Message,
)
from purplship.providers.purolator.package import (
    parse_track_package_response,
    track_package_by_pin_request,
    parse_full_estimate_response,
    get_full_estimate_request,
    parse_shipment_creation_response,
    create_shipment_request,
)


class Mapper(BaseMapper):
    settings: Settings

    """Request Mappers"""

    def create_rate_request(self, payload: RateRequest) -> Serializable[Element]:
        return get_full_estimate_request(payload, self.settings)

    def create_tracking_request(
        self, payload: TrackingRequest
    ) -> Serializable[Element]:
        return track_package_by_pin_request(payload, self.settings)

    def create_shipment_request(
        self, payload: ShipmentRequest
    ) -> Serializable[Element]:
        return create_shipment_request(payload, self.settings)

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
