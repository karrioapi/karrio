from typing import List, Tuple
from karrio.core.utils.serializable import Serializable, Deserializable
from karrio.api.mapper import Mapper as BaseMapper
from karrio.core.models import (
    RateDetails,
    RateRequest,
    Message,
    ShipmentDetails,
)
from karrio.universal.providers.shipping import (
    parse_shipment_response,
    shipment_request,
)
from karrio.universal.providers.rating import (
    parse_rate_response,
    rate_request,
)
from karrio.mappers.generic.settings import Settings


class Mapper(BaseMapper):
    settings: Settings

    def create_rate_request(self, payload: RateRequest) -> Serializable:
        return rate_request(payload, self.settings)

    def create_shipment_request(self, payload: Serializable) -> Serializable:
        return shipment_request(payload, self.settings)

    def parse_rate_response(
        self, response: Deserializable
    ) -> Tuple[List[RateDetails], List[Message]]:
        return parse_rate_response(response, self.settings)

    def parse_shipment_response(
        self, response: Deserializable
    ) -> Tuple[ShipmentDetails, List[Message]]:
        return parse_shipment_response(response, self.settings)
