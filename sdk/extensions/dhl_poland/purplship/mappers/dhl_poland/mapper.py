from typing import List, Tuple
from purplship.core.utils.serializable import Serializable, Deserializable
from purplship.api.mapper import Mapper as BaseMapper
from purplship.core.models import (
    RateDetails,
    RateRequest,
    TrackingRequest,
    TrackingDetails,
    Message,
)
from purplship.universal.providers.rating import parse_rate_response, rate_request
from purplship.providers.dhl_poland import (
    parse_shipment_cancel_response,
    parse_shipment_response,
    shipment_cancel_request,
    shipment_request,
)
from purplship.mappers.dhl_poland.settings import Settings


class Mapper(BaseMapper):
    settings: Settings

    def create_rate_request(self, payload: RateRequest) -> Serializable:
        return rate_request(payload, self.settings)

    def create_shipment_request(self, payload: Serializable[str]) -> Serializable:
        return shipment_request(payload, self.settings)

    def create_cancel_shipment_request(self, payload: TrackingRequest) -> Serializable:
        return shipment_cancel_request(payload, self.settings)

    def parse_rate_response(
        self, response: Deserializable[str]
    ) -> Tuple[List[RateDetails], List[Message]]:
        return parse_rate_response(response.deserialize(), self.settings)

    def parse_shipment_response(
        self, response: Deserializable[str]
    ) -> Tuple[TrackingDetails, List[Message]]:
        return parse_shipment_response(response.deserialize(), self.settings)

    def parse_cancel_shipment_response(
        self, response: Deserializable[str]
    ) -> Tuple[TrackingDetails, List[Message]]:
        return parse_shipment_cancel_response(response.deserialize(), self.settings)
