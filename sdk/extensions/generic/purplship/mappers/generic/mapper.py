from typing import List, Tuple
from purplship.core.utils.serializable import Serializable, Deserializable
from purplship.api.mapper import Mapper as BaseMapper
from purplship.core.models import (
    RateDetails,
    RateRequest,
    Message,
    ShipmentDetails,
)
from purplship.universal.providers import (
    parse_shipment_response,
    parse_rate_response,
    shipment_request,
    rate_request,
)
from purplship.mappers.generic.settings import Settings


class Mapper(BaseMapper):
    settings: Settings

    def create_rate_request(self, payload: RateRequest) -> Serializable:
        return rate_request(payload, self.settings)

    def create_shipment_request(self, payload: Serializable[str]) -> Serializable:
        return shipment_request(payload, self.settings)

    def parse_rate_response(
        self, response: Deserializable[str]
    ) -> Tuple[List[RateDetails], List[Message]]:
        return parse_rate_response(response.deserialize(), self.settings)

    def parse_shipment_response(
        self, response: Deserializable[str]
    ) -> Tuple[ShipmentDetails, List[Message]]:
        return parse_shipment_response(response.deserialize(), self.settings)
