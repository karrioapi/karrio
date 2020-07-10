from typing import List, Tuple
from purplship.package.mapper import Mapper as BaseMapper
from purplship.package.mappers.freightcom.settings import Settings
from purplship.core.utils.serializable import Deserializable, Serializable
from purplship.core.utils.xml import Element
from purplship.core.models import (
    RateRequest,
    ShipmentRequest,
    ShipmentDetails,
    RateDetails,
    Message,
)
from purplship.carriers.freightcom import (
    parse_quote_reply,
    quote_request,
    parse_shipping_reply,
    shipping_request,
)


class Mapper(BaseMapper):
    settings: Settings

    """Request Mappers"""

    def create_rate_request(self, payload: RateRequest) -> Serializable[Element]:
        return quote_request(payload, self.settings)

    def create_shipment_request(
        self, payload: ShipmentRequest
    ) -> Serializable[Element]:
        return shipping_request(payload, self.settings)

    """Response Parsers"""

    def parse_rate_response(
        self, response: Deserializable[str]
    ) -> Tuple[List[RateDetails], List[Message]]:
        return parse_quote_reply(response.deserialize(), self.settings)

    def parse_shipment_response(
        self, response: Deserializable[str]
    ) -> Tuple[ShipmentDetails, List[Message]]:
        return parse_shipping_reply(response.deserialize(), self.settings)
