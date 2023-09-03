import karrio.lib as lib
from typing import List, Tuple
from karrio.schemas.canpar.CanparRatingService import (
    searchCanadaPost,
    SearchCanadaPostRq,
    Address as CanparAddress,
)
import karrio.lib as lib
from karrio.core.models import (
    AddressValidationDetails,
    AddressValidationRequest,
    Message,
    Address,
)
from karrio.core.utils import (
    create_envelope,
    Element,
    Serializable,
    SF,
    XP,
)
from karrio.providers.canpar.error import parse_error_response
from karrio.providers.canpar.utils import Settings


def parse_address_validation_response(
    _response: lib.Deserializable[Element],
    settings: Settings,
) -> Tuple[AddressValidationDetails, List[Message]]:
    response = _response.deserialize()
    errors = parse_error_response(response, settings)
    address = lib.find_element("address", response, CanparAddress, first=True)

    success = len(errors) == 0
    validation_details = (
        AddressValidationDetails(
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
                address_line2=SF.concat_str(
                    address.address_line_2, address.address_line_3, join=True
                ),
            ),
        )
        if success
        else None
    )

    return validation_details, errors


def address_validation_request(
    payload: AddressValidationRequest,
    settings: Settings,
) -> Serializable:
    address = lib.to_address(payload.address)

    request = create_envelope(
        body_content=searchCanadaPost(
            request=SearchCanadaPostRq(
                city=payload.address.city or "",
                password=settings.password,
                postal_code=payload.address.postal_code or "",
                province=payload.address.state_code or "",
                street_direction="",
                street_name=address.street_name or "",
                street_num=address.street_number or "",
                street_type="",
                user_id=settings.username,
                validate_only=True,
            )
        )
    )

    return Serializable(request, Settings.serialize)
