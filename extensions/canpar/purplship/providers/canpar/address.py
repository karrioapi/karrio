from typing import List, Tuple
from canpar_lib.CanparRatingService import (
    searchCanadaPost,
    SearchCanadaPostRq,
    Address as CanparAddress
)
from purplship.core.models import (
    AddressValidationDetails,
    AddressValidationRequest,
    Message,
    Address
)
from purplship.core.utils import (
    create_envelope,
    Element,
    Envelope,
    Serializable,
    SF,
    XP,
)
from purplship.providers.canpar.error import parse_error_response
from purplship.providers.canpar.utils import Settings


def parse_address_validation_response(response: Element, settings: Settings) -> Tuple[AddressValidationDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    address_node = next(iter(response.xpath(".//*[local-name() = $name]", name="address")), None)
    address = XP.build(CanparAddress, address_node)
    success = len(errors) == 0
    validation_details = AddressValidationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success=success,
        complete_address=Address(
            postal_code=address.postal_code,
            city=address.city,
            company_name=address.name,
            country_code=address.country,
            email=address.email,
            state_code=address.province,
            residential=address.residential,
            address_line1=address.address_line_1,
            address_line2=SF.concat_str(address.address_line_2, address.address_line_3, join=True)
        )
    ) if success else None

    return validation_details, errors


def address_validation_request(payload: AddressValidationRequest, settings: Settings) -> Serializable[Envelope]:

    request = create_envelope(
        body_content=searchCanadaPost(
            request=SearchCanadaPostRq(
                city=payload.address.city or "",
                password=settings.password,
                postal_code=payload.address.postal_code or "",
                province=payload.address.state_code or "",
                street_direction="",
                street_name=SF.concat_str(payload.address.address_line1, payload.address.address_line2, join=True) or "",
                street_num="",
                street_type="",
                user_id=settings.username,
                validate_only=True
            )
        )
    )

    return Serializable(request, Settings.serialize)
