from typing import Tuple, List, Union
from purplship.domain.mapper import Mapper
from purplship.domain.Types import (
    RateRequest,
    TrackingRequest,
    Error,
    QuoteDetails,
    TrackingDetails
)
from .partials import (
    SendleRateMapperPartial,
    SendleTrackMapperPartial,
)
from pysendle.quotes import DomesticParcelQuote, InternationalParcelQuote

ParcelQuoteRequest = Union[DomesticParcelQuote, InternationalParcelQuote]


class SendleMapper(
    Mapper,
    SendleRateMapperPartial,
    SendleTrackMapperPartial,
):

    """Request Mappers"""

    def create_quote_request(self, payload: RateRequest) -> ParcelQuoteRequest:
        return self.create_parcel_quote_request(payload)

    def create_tracking_request(self, payload: TrackingRequest) -> List[str]:
        return self.create_parcel_tracking_request(payload)

    """Response Parsers"""

    def parse_quote_response(self, response: dict) -> Tuple[List[QuoteDetails], List[Error]]:
        return self.parse_parcel_quote_response(response)

    def parse_tracking_response(self, response: dict) -> Tuple[List[TrackingDetails], List[Error]]:
        return self.parse_parcel_tracking_response(response)
