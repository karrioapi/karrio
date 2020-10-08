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
)
from purplship.providers.canpar import (
)
from purplship.mappers.canpar.settings import Settings


class Mapper(BaseMapper):
    settings: Settings

    """Request Mappers"""

    def create_rate_request(
        self, payload: RateRequest
    ) -> Serializable:
        pass

    def create_tracking_request(
        self, payload: TrackingRequest
    ) -> Serializable:
        pass

    def create_shipment_request(
        self, payload: ShipmentRequest
    ) -> Serializable:
        pass

    """Response Parsers"""

    def parse_rate_response(
        self, response: Deserializable[str]
    ) -> Tuple[List[RateDetails], List[Message]]:
        pass

    def parse_tracking_response(
        self, response: Deserializable[str]
    ) -> Tuple[List[TrackingDetails], List[Message]]:
        pass

    def parse_shipment_response(
        self, response: Deserializable[str]
    ) -> Tuple[ShipmentDetails, List[Message]]:
        pass
