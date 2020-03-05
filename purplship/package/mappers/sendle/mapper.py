from typing import List, Union
from purplship.package.mapper import Mapper as BaseMapper
from purplship.package.mappers.sendle.settings import Settings
from purplship.core.utils.serializable import Serializable, Deserializable
from purplship.core.models import (
    RateRequest,
    TrackingRequest,
    Error,
    RateDetails,
    TrackingDetails
)
from purplship.carriers.sendle import (
    parse_parcel_quote_response, parcel_quote_request,
    parcel_tracking_request, parse_parcel_tracking_response
)
from pysendle.quotes import DomesticParcelQuote, InternationalParcelQuote

ParcelQuoteRequest = Union[DomesticParcelQuote, InternationalParcelQuote]


class Mapper(BaseMapper):
    settings: Settings

    """Request Mappers"""

    def create_rate_request(self, payload: RateRequest) -> Serializable[ParcelQuoteRequest]:
        return parcel_quote_request(payload, self.settings)

    def create_tracking_request(self, payload: TrackingRequest) -> Serializable[List[str]]:
        return parcel_tracking_request(payload)

    """Response Parsers"""

    def parse_rate_response(self, response: Deserializable[str]) -> (List[RateDetails], List[Error]):
        return parse_parcel_quote_response(response.deserialize(), self.settings)

    def parse_tracking_response(self, response: Deserializable[str]) -> (List[TrackingDetails], List[Error]):
        return parse_parcel_tracking_response(response.deserialize(), self.settings)
