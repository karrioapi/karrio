from typing import Tuple, List
from usps_lib.address_validate_request import AddressValidateRequest, AddressType
from purplship.core.utils import Serializable, Element, SF, XP
from purplship.core.models import AddressValidationRequest, Message, AddressValidationDetails

from purplship.providers.usps.utils import Settings
from purplship.providers.usps.error import parse_error_response


def parse_address_validation_response(response: Element, settings: Settings) -> Tuple[AddressValidationDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    details = None

    return details, errors


def address_validation_request(payload: AddressValidationRequest, settings: Settings) -> Serializable[AddressValidateRequest]:

    request = AddressValidateRequest(
        USERID=settings.username,
        Revision="1",
        Address=AddressType(
            ID=None,
            FirmName=(payload.address.company_name or payload.address.person_name),
            Address1=payload.address.address_line1,
            Address2=SF.concat_str(payload.address.address_line1, payload.address.address_line2, join=True),
            City=payload.address.city,
            State=payload.address.state_code,
            Urbanization=None,
            Zip5=payload.address.postal_code,
            Zip4=None,
        )
    )

    return Serializable(request, XP.export)
