from typing import Tuple, List, Union
from gds_helpers import to_dict
from purplship.mappers.aups import AustraliaPostClient
from purplship.domain.Types import (
    QuoteDetails,
    RateRequest,
    Error
)
from pyaups.domestic_letter_postage import ServiceRequest as DomesticLetterServiceRequest
from pyaups.international_letter_postage import ServiceRequest as IntlLetterServiceRequest
from pyaups.domestic_parcel_postage import ServiceRequest as DomesticParcelServiceRequest
from pyaups.international_parcel_postage import ServiceRequest as IntlParcelServiceRequest
from pyaups.error import ErrorResponse, APIError, PostageError

PostageRequest = Union[
    DomesticLetterServiceRequest,
    DomesticParcelServiceRequest,
    IntlLetterServiceRequest,
    IntlParcelServiceRequest
]


class AustraliaPostCapabilities:
    """
        AustraliaPost native service request types
    """

    """ Requests """

    def create_service_request(self, payload: RateRequest) -> PostageRequest:
        pass

    """ Replys """

    def parse_service_response(self, response: dict) -> Tuple[List[QuoteDetails], List[Error]]:
        pass


class AustraliaPostMapperBase(AustraliaPostCapabilities):
    """
        AustraliaPost mapper base class
    """

    def __init__(self, client: AustraliaPostClient):
        self.client: AustraliaPostClient = client

    def parse_error_response(self, response: dict) -> List[Error]:
        error_response: ErrorResponse = ErrorResponse(**response)
        errors: List[Union[APIError, PostageError]] = error_response.error + error_response.errors
        return [
            Error(
                carrier=self.client.carrier_name,
                code=error.get('code') or error.get('error_code'),
                message=error.get('message') or error.get('errorMessage')
            ) for error in to_dict(errors)
        ]
