from typing import Tuple, List
from pypurolator.service_availability_service_2_0_2 import (
    ValidateCityPostalCodeZipRequest,
    ArrayOfShortAddress,
    ShortAddress,
)
from purplship.core.utils import Serializable, export, Element
from purplship.core.models import AddressValidationRequest, Message, AddressValidationDetails
from purplship.providers.purolator.utils import Settings
from purplship.providers.purolator.error import parse_error_response


def parse_validate_address_response(response: Element, settings: Settings) -> Tuple[AddressValidationDetails, List[Message]]:
    validation_details = _extract_address_validation(response, settings)
    return validation_details, parse_error_response(response, settings)


def _extract_address_validation(node: Element, settings: Settings) -> AddressValidationDetails:

    return AddressValidationDetails(
        carrier=settings.carrier,
        carrier_name=settings.carrier_name,
    )


def validate_address_request(payload: AddressValidationRequest, settings: Settings) -> Serializable[ValidateCityPostalCodeZipRequest]:

    request = ValidateCityPostalCodeZipRequest(
        Addresses=ArrayOfShortAddress(
            ShortAddress=[
                ShortAddress(
                    City=None,
                    Province=None,
                    Country=None,
                    PostalCode=None,
                )
            ]
        )
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: ValidateCityPostalCodeZipRequest) -> str:
    namespacedef_ = ''

    return export(
        request,
        namespacedef_=namespacedef_
    )
