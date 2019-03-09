from typing import Tuple, List, Union
from purplship.mappers.sendle import SendleClient
from purplship.domain.Types import (
    RateRequest,
    TrackingRequest,
    Error,
    TrackingDetails,
    QuoteDetails
)
from pysendle.quotes import DomesticParcelQuote, InternationalParcelQuote
from pysendle.validation_error import ValidationError

ParcelQuoteRequest = Union[DomesticParcelQuote, InternationalParcelQuote]


class SendleCapabilities:
    """
        Sendle native service request types
    """

    """ Requests Mappers """

    def create_parcel_quote_request(self, payload: RateRequest) -> ParcelQuoteRequest:
        pass

    def create_parcel_tracking_request(self, payload: TrackingRequest) -> List[str]:
        pass

    """ Response Parsing """

    def parse_parcel_quote_response(self, response: dict) -> Tuple[List[QuoteDetails], List[Error]]:
        pass

    def parse_parcel_tracking_response(self, response: dict) -> Tuple[List[TrackingDetails], List[Error]]:
        pass


class SendleMapperBase(SendleCapabilities):
    """Sendle mapper base class."""

    def __init__(self, client: SendleClient):
        self.client: SendleClient = client

    def parse_error_response(self, response: List[dict]) -> List[Error]:
        errors: List[ValidationError] = [
            ValidationError(**e) for e in response
            if 'error' in e
        ]
        return [
            Error(
                code=error.error,
                carrier=self.client.carrier_name,
                message=error.error_description,
                details=error.messages
            ) for error in errors
        ]
