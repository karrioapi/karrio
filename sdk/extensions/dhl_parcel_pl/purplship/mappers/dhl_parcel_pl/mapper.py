from typing import List, Tuple
from purplship.core.utils.serializable import Serializable, Deserializable
from purplship.api.mapper import Mapper as BaseMapper
from purplship.core.models import (
    TrackingRequest,
    TrackingDetails,
    Message,
)
from purplship.providers.dhl_parcel_pl import (
    parse_tracking_response,
    tracking_request,
)
from purplship.mappers.dhl_parcel_pl.settings import Settings


class Mapper(BaseMapper):
    settings: Settings

    def create_tracking_request(self, payload: TrackingRequest) -> Serializable:
        return tracking_request(payload, self.settings)

    def parse_tracking_response(
        self, response: Deserializable[str]
    ) -> Tuple[List[TrackingDetails], List[Message]]:
        return parse_tracking_response(response.deserialize(), self.settings)
