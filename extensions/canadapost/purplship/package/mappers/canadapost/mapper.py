from typing import List, Tuple
from pycanadapost.rating import mailing_scenario
from purplship.core.utils.pipeline import Pipeline
from purplship.core.utils.serializable import Serializable, Deserializable
from purplship.package.mapper import Mapper as BaseMapper
from purplship.core.models import (
    ShipmentRequest,
    TrackingRequest,
    Message,
    TrackingDetails,
    RateDetails,
    RateRequest,
    ShipmentDetails,
)
from purplship.carriers.canadapost import (
    mailing_scenario_request,
    parse_price_quotes,
    tracking_pins_request,
    parse_tracking_summary,
    shipment_request,
    parse_shipment_response,
)
from purplship.package.mappers.canadapost.settings import Settings


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
