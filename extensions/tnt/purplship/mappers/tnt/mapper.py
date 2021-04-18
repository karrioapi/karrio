from typing import List, Tuple
from purplship.core.utils.serializable import Serializable, Deserializable
from purplship.api.mapper import Mapper as BaseMapper
from purplship.core.models import (
    # ShipmentRequest,
    TrackingRequest,
    RateRequest,

    TrackingDetails,
    # ShipmentDetails,
    RateDetails,
    Message,
)
from purplship.providers.tnt import (
    # parse_shipment_response,
    parse_tracking_response,
    # parse_rate_response,

    tracking_request,
    # shipment_request,
    # rate_request,
)
from purplship.mappers.tnt.settings import Settings


class Mapper(BaseMapper):
    settings: Settings

    """Request Mappers"""

    # def create_rate_request(
    #     self, payload: RateRequest
    # ) -> Serializable:
    #     return rate_request(payload, self.settings)

    # def create_shipment_request(
    #     self, payload: ShipmentRequest
    # ) -> Serializable:
    #     return shipment_request(payload, self.settings)

    def create_tracking_request(
        self, payload: TrackingRequest
    ) -> Serializable:
        return tracking_request(payload, self.settings)

    """Response Parsers"""

    # def parse_rate_response(
    #     self, response: Deserializable[str]
    # ) -> Tuple[List[RateDetails], List[Message]]:
    #     return parse_rate_response(response.deserialize(), self.settings)

    # def parse_shipment_response(
    #     self, response: Deserializable[str]
    # ) -> Tuple[ShipmentDetails, List[Message]]:
    #     return parse_shipment_response(response.deserialize(), self.settings)

    def parse_tracking_response(
        self, response: Deserializable[str]
    ) -> Tuple[List[TrackingDetails], List[Message]]:
        return parse_tracking_response(response.deserialize(), self.settings)
