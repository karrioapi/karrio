from typing import Tuple, List
from purplship.domain.mapper import Mapper
from purplship.domain.Types import (
    RateRequest,
    TrackingRequest,
    Error,
    QuoteDetails,
    TrackingDetails
)
from .partials import (
    AustraliaPostRateMapperPartial,
    AustraliaPostTrackMapperPartial,
)
from pyaups.shipping_price_request import ShippingPriceRequest


class AustraliaPostMapper(
    Mapper,
    AustraliaPostRateMapperPartial,
    AustraliaPostTrackMapperPartial,
):
    def create_quote_request(self, payload: RateRequest) -> ShippingPriceRequest:
        return self.create_shipping_price_request(payload)

    def create_tracking_request(self, payload: TrackingRequest) -> List[str]:
        return self.create_track_items_request(payload)

    def parse_quote_response(self, response: dict) -> Tuple[List[QuoteDetails], List[Error]]:
        return self.parse_shipping_price_response(response)

    def parse_tracking_response(self, response: dict) -> Tuple[List[TrackingDetails], List[Error]]:
        return self.parse_track_items_response(response)
