from typing import Tuple, List
from purolator_lib.service_availability_service_2_0_2 import (
    ValidateCityPostalCodeZipRequest,
    ValidateCityPostalCodeZipResponse,
    ArrayOfShortAddress,
    ShortAddress,
    RequestContext,
)
from purplship.core.utils import Serializable, Element, create_envelope, Envelope, XP
from purplship.core.models import AddressValidationRequest, Message, AddressValidationDetails, Address
from purplship.providers.purolator_courier.utils import Settings, standard_request_serializer
from purplship.providers.purolator_courier.error import parse_error_response


def parse_address_validation_response(response: Element, settings: Settings) -> Tuple[AddressValidationDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    reply = XP.build(
        ValidateCityPostalCodeZipResponse,
        next(iter(response.xpath(".//*[local-name() = $name]", name="ValidateCityPostalCodeZipResponse")), None)
    )
    address: ShortAddress = next((result.Address for result in reply.SuggestedAddresses.SuggestedAddress), None)
    success = len(errors) == 0
    validation_details = AddressValidationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success=success,
        complete_address=Address(
            city=address.City,
            state_code=address.Province,
            country_code=address.Country,
            postal_code=address.PostalCode
        ) if address is not None else None
    ) if success else None

    return validation_details, errors


def address_validation_request(payload: AddressValidationRequest, settings: Settings) -> Serializable[Envelope]:

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
        )
    )

    return Serializable(request, standard_request_serializer)
