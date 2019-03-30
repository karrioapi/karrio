from typing import Tuple, List, Union
from lxml import etree
from purplship.domain.mapper import Mapper
from purplship.domain.Types import (
    RateRequest,
    TrackingRequest,
    TrackingDetails,
    QuoteDetails,
    Error,
)
from pyusps.ratev4request import RateV4Request
from pyusps.intlratev2request import IntlRateV2Request
from pyusps.trackfieldrequest import TrackFieldRequest
from .partials import USPSRateMapperPartial, USPSTrackMapperPartial


class USPSMapper(Mapper, USPSRateMapperPartial, USPSTrackMapperPartial):
    def create_quote_request(
        self, payload: RateRequest
    ) -> Union[RateV4Request, IntlRateV2Request]:
        return self.create_rate_request(payload)

    def create_tracking_request(self, payload: TrackingRequest) -> TrackFieldRequest:
        return self.create_track_request(payload)

    """Parser"""

    def parse_quote_response(
        self, response: etree.ElementBase
    ) -> Tuple[List[QuoteDetails], List[Error]]:
        return self.parse_rate_response(response)

    def parse_tracking_response(
        self, response: etree.ElementBase
    ) -> Tuple[List[TrackingDetails], List[Error]]:
        return self.parse_track_response(response)
