from typing import List
from pyaups.shipping_price_request import ShippingPriceRequest
from purplship.carriers.aups.shipping import (
    shipping_price_request, parse_shipping_price_response,
    track_items_request, parse_track_items_response
)
from purplship.core.utils.serializable import Deserializable, Serializable
from purplship.package.mapper import Mapper as BaseMapper
from purplship.core.models import (
    RateRequest, TrackingRequest, Error, RateDetails, TrackingDetails
)
from purplship.package.mappers.aups.settings import Settings


class Mapper(BaseMapper):
    settings: Settings
    
    def create_rate_request(self, payload: RateRequest) -> Serializable[ShippingPriceRequest]:
        return shipping_price_request(payload)

    def parse_rate_response(self, response: Deserializable[str]) -> (List[RateDetails], List[Error]):
        return parse_shipping_price_response(response.deserialize(), self.settings)

    def create_tracking_request(self, payload: TrackingRequest) -> Serializable[List[str]]:
        return track_items_request(payload)

    def parse_tracking_response(self, response: Deserializable[str]) -> (List[TrackingDetails], List[Error]):
        return parse_track_items_response(response.deserialize(), self.settings)
