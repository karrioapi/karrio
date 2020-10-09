from typing import List, Tuple
from pycanpar.CanparRatingService import (
    searchCanadaPost,
    SearchCanadaPostRq
)
from purplship.core.models import (
    AddressValidationDetails,
    AddressValidationRequest,
    Message,
)
from purplship.core.utils import (
    create_envelope,
    Element,
    Envelope,
    Serializable,
    concat_str
)
from purplship.providers.canpar.error import parse_error_response
from purplship.providers.canpar.utils import Settings, default_request_serializer


def parse_search_response(response: Element, settings: Settings) -> Tuple[AddressValidationDetails, List[Message]]:
    confirmation: AddressValidationDetails = None

    return confirmation, parse_error_response(response, settings)


def search_canada_post(payload: AddressValidationRequest, settings: Settings) -> Serializable[Envelope]:

    request = create_envelope(
        body_content=searchCanadaPost(
            request=SearchCanadaPostRq(
                city=payload.address.city,
                password=settings.password,
                postal_code=payload.address.postal_code,
                province=payload.address.state_code,
                street_direction="",
                street_name=concat_str(payload.address.address_line1, payload.address.address_line2, join=True),
                street_num="",
                street_type="",
                user_id=settings.user_id,
                validate_only=True
            )
        )
    )

    return Serializable(request, default_request_serializer)
