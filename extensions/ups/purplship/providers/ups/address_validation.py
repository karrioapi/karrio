from typing import Tuple, List
from pyups.av_request import (
    AddressValidationRequest as UPSAddressValidationRequest,
    AddressType,
    RequestType
)
from purplship.core.utils import Serializable, export, Element
from purplship.core.models import AddressValidationRequest, Message, AddressValidationDetails
from purplship.core.utils.soap import create_envelope
from purplship.providers.ups.utils import Settings
from purplship.providers.ups.error import parse_error_response


def parse_address_validation_response(response: Element, settings: Settings) -> Tuple[AddressValidationDetails, List[Message]]:
    validation_details = _extract_address_validation(response, settings)
    return validation_details, parse_error_response(response, settings)


def _extract_address_validation(node: Element, settings: Settings) -> AddressValidationDetails:

    return AddressValidationDetails(
        carrier=settings.carrier,
        carrier_name=settings.carrier_name,
    )


def address_validation_request(payload: AddressValidationRequest, settings: Settings) -> Serializable[UPSAddressValidationRequest]:

    request = UPSAddressValidationRequest(
        Request=RequestType(
            TransactionReference=None,
            RequestAction=None,
        ),
        Address=AddressType(
            City=payload.address.city,
            StateProvinceCode=payload.address.state_code,
            CountryCode=payload.address.country_code,
            PostalCode=payload.address.postal_code
        ),
    )
    return Serializable(
        create_envelope(header_content=settings.Security, body_content=request),
        _request_serializer,
    )


def _request_serializer(request: UPSAddressValidationRequest) -> str:
    namespacedef_ = ''

    return export(
        request,
        namespacedef_=namespacedef_
    )
