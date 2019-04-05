from typing import Tuple, List
from purplship.domain.mapper import Mapper
from purplship.domain.Types import (
    RateRequest,
    Error,
    QuoteDetails,
)
from .partials import AustraliaPostRateMapperPartial
from pyaups.shipping_price_request import ShippingPriceRequest


class AustraliaPostMapper(
    Mapper,
    AustraliaPostRateMapperPartial,
):
    def create_quote_request(self, payload: RateRequest) -> ShippingPriceRequest:
        return self.create_service_request(payload)

    def parse_quote_response(self, response: dict) -> Tuple[List[QuoteDetails], List[Error]]:
        return self.parse_service_response(response)
