from typing import List, Union, Tuple
from pyusps.ratev4request import RateV4Request
from pyusps.intlratev2request import IntlRateV2Request
from pyusps.trackfieldrequest import TrackFieldRequest
from purplship.api.mapper import Mapper as BaseMapper
from purplship.api.mappers.usps.settings import Settings
from purplship.core.utils.serializable import Serializable, Deserializable
from purplship.core.models import (
    RateRequest,
    TrackingRequest,
    TrackingDetails,
    RateDetails,
    Message,
)
from purplship.providers.usps import (
    rate_request,
    parse_rate_request,
    track_field_request,
    parse_track_field_response,
)


class Mapper(BaseMapper):
    settings: Settings

    """Request Mappers"""

    def create_rate_request(
        self, payload: RateRequest
    ) -> Serializable[Union[RateV4Request, IntlRateV2Request]]:
        return rate_request(payload, self.settings)

    def create_tracking_request(
        self, payload: TrackingRequest
    ) -> Serializable[TrackFieldRequest]:
        return track_field_request(payload, self.settings)

    """Response Parsers"""

    def parse_rate_response(
        self, response: Deserializable[str]
    ) -> Tuple[List[RateDetails], List[Message]]:
        return parse_rate_request(response.deserialize(), self.settings)

    def parse_tracking_response(
        self, response: Deserializable[str]
    ) -> Tuple[List[TrackingDetails], List[Message]]:
        return parse_track_field_response(response.deserialize(), self.settings)
