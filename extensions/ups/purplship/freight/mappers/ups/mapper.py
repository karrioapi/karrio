from typing import List, Tuple
from purplship.freight.mapper import Mapper as BaseMapper
from purplship.freight.mappers.ups.settings import Settings
from purplship.core.utils.serializable import Deserializable, Serializable
from purplship.core.models import (
    RateRequest,
    ShipmentRequest,
    TrackingRequest,
    ShipmentDetails,
    RateDetails,
    TrackingDetails,
    Message,
)
from purplship.carriers.ups.package import parse_track_response, track_request

from purplship.carriers.ups.freight import (
    freight_ship_request,
    parse_freight_ship_response,
    freight_rate_request,
    parse_freight_rate_response,
)
from pyups.freight_rate_web_service_schema import FreightRateRequest
from pyups.track_web_service_schema import TrackRequest
from pyups.freight_ship_web_service_schema import FreightShipRequest


class Mapper(BaseMapper):
    settings: Settings

    """Request Mappers"""

    def create_rate_request(
        self, payload: RateRequest
    ) -> Serializable[FreightRateRequest]:
        return freight_rate_request(payload, self.settings)

    def create_tracking_request(
        self, payload: TrackingRequest
    ) -> Serializable[List[TrackRequest]]:
        return track_request(payload, self.settings)

    def create_shipment_request(
        self, payload: ShipmentRequest
    ) -> Serializable[FreightShipRequest]:
        return freight_ship_request(payload, self.settings)

    """Response Parsers"""

    def parse_rate_response(
        self, response: Deserializable[str]
    ) -> Tuple[List[RateDetails], List[Message]]:
        return parse_freight_rate_response(response.deserialize(), self.settings)

    def parse_tracking_response(
        self, response: Deserializable[str]
    ) -> Tuple[List[TrackingDetails], List[Message]]:
        return parse_track_response(response.deserialize(), self.settings)

    def parse_shipment_response(
        self, response: Deserializable[str]
    ) -> Tuple[ShipmentDetails, List[Message]]:
        return parse_freight_ship_response(response.deserialize(), self.settings)
