from typing import Tuple, List
from karrio.schemas.purolator.service_availability_service_2_0_2 import (
    ValidateCityPostalCodeZipRequest,
    ValidateCityPostalCodeZipResponse,
    ArrayOfShortAddress,
    ShortAddress,
    RequestContext,
)
from karrio.core.utils import Serializable, Element, create_envelope, XP
from karrio.core.models import (
    AddressValidationRequest,
    Message,
    AddressValidationDetails,
    Address,
)
from karrio.providers.purolator.utils import Settings, standard_request_serializer
from karrio.providers.purolator.error import parse_error_response
import karrio.lib as lib


def parse_address_validation_response(
    _response: lib.Deserializable[Element], settings: Settings
) -> Tuple[AddressValidationDetails, List[Message]]:
    response = _response.deserialize()
    errors = parse_error_response(response, settings)
    reply = XP.to_object(
        ValidateCityPostalCodeZipResponse,
        lib.find_element("ValidateCityPostalCodeZipResponse", response, first=True),
    )
    address: ShortAddress = next(
        (result.Address for result in reply.SuggestedAddresses.SuggestedAddress), None
    )
    success = len(errors) == 0
    validation_details = (
        AddressValidationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=success,
            complete_address=Address(
                city=address.City,
                state_code=address.Province,
                country_code=address.Country,
                postal_code=address.PostalCode,
            )
            if address is not None
            else None,
        )
        if success
        else None
    )

    return validation_details, errors


def address_validation_request(
    payload: AddressValidationRequest, settings: Settings
) -> Serializable:
    request = create_envelope(
        header_content=RequestContext(
            Version="2.1",
            Language=settings.language,
            GroupID="",
            RequestReference="",
            UserToken=settings.user_token,
        ),
        body_content=ValidateCityPostalCodeZipRequest(
            Addresses=ArrayOfShortAddress(
                ShortAddress=[
                    ShortAddress(
                        City=payload.address.city,
                        Province=payload.address.state_code,
                        Country=payload.address.country_code,
                        PostalCode=payload.address.postal_code,
                    )
                ]
            )
        ),
    )

    return Serializable(request, standard_request_serializer)
