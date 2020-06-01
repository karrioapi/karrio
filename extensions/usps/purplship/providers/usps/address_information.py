from typing import Tuple, List
from pyusps.addressvalidaterequest import (
    AddressValidateRequest,
    AddressType
)
from purplship.core.utils import Serializable, export, Element, concat_str
from purplship.core.models import AddressValidationRequest, Message, AddressValidationDetails
from purplship.carriers.purolator.utils import Settings
from purplship.carriers.purolator.error import parse_error_response


def parse_address_validate_response(response: Element, settings: Settings) -> Tuple[AddressValidationDetails, List[Message]]:
    validation_details = _extract_address_validation(response, settings)
    return validation_details, parse_error_response(response, settings)


def _extract_address_validation(node: Element, settings: Settings) -> AddressValidationDetails:

    return AddressValidationDetails(
        carrier=settings.carrier,
        carrier_name=settings.carrier_name,
    )


def address_validate_request(payload: AddressValidationRequest, settings: Settings) -> Serializable[AddressValidateRequest]:

    request = AddressValidateRequest(
        USERID=None,
        Revision=None,
        Address=AddressType(
            ID=None,
            Address1=concat_str(payload.address.address_line1),
            Address2=concat_str(payload.address.address_line2),
            City=payload.address.city,
            FirmName=payload.address.company_name,
            State=payload.address.state_code,
            Zip5=None,
            Zip4=None,
        )
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: AddressValidateRequest) -> str:
    namespacedef_ = ''

    return export(
        request,
        namespacedef_=namespacedef_
    )
