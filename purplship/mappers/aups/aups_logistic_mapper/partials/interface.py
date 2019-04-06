from typing import Tuple, List
from purplship.mappers.aups import AustraliaPostClient
from purplship.domain.Types import (
    RateRequest,
    TrackingRequest,
    Error,
    TrackingDetails,
    QuoteDetails
)
from pyaups.shipping_price_request import ShippingPriceRequest
from pyaups.shipping_price_response import Errors


class AustraliaPostCapabilities:
    """
        AustraliaPost native service request types
    """

    """ Requests """

    def create_shipping_price_request(self, payload: RateRequest) -> ShippingPriceRequest:
        pass

    def create_track_items_request(self, payload: TrackingRequest) -> List[str]:
        pass

    """ Replys """

    def parse_shipping_price_response(self, response: dict) -> Tuple[List[QuoteDetails], List[Error]]:
        pass

    def parse_track_items_response(self, response: dict) -> Tuple[List[TrackingDetails], List[Error]]:
        pass


class AustraliaPostMapperBase(AustraliaPostCapabilities):
    """
        AustraliaPost mapper base class
    """

    def __init__(self, client: AustraliaPostClient):
        self.client: AustraliaPostClient = client

    def parse_error_response(self, response: dict) -> List[Error]:
        if 'errors' in response:
            return [
                Error(
                    message=error.get('message'),
                    carrier=self.client.carrier_name,
                    code=error.get('code') or error.get('error_code')
                ) for error in response.get('errors', [])
            ]
        return []
