from functools import partial

import karrio.lib as lib
from karrio.core.models import (
    ConfirmationDetails,
    Message,
    PickupCancelRequest,
)
from karrio.core.utils import Element, Serializable, create_envelope
from karrio.providers.purolator.error import parse_error_response
from karrio.providers.purolator.utils import Settings, standard_request_serializer
from karrio.schemas.purolator.pickup_service_1_2_1 import (
    RequestContext,
    VoidPickUpRequest,
)


def parse_pickup_cancel_response(
    _response: lib.Deserializable[Element],
    settings: Settings,
) -> tuple[ConfirmationDetails, list[Message]]:
    response = _response.deserialize()
    errors = parse_error_response(response, settings)
    cancellation = (
        ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=True,
            operation="Cancel Pickup",
        )
        if not any(errors)
        else None
    )

    return cancellation, errors


def pickup_cancel_request(payload: PickupCancelRequest, settings: Settings) -> Serializable:
    request = create_envelope(
        header_content=RequestContext(
            Version="1.2",
            Language=settings.language,
            GroupID="",
            RequestReference="",
            UserToken=settings.user_token,
        ),
        body_content=VoidPickUpRequest(PickUpConfirmationNumber=payload.confirmation_number),
    )

    return Serializable(request, partial(standard_request_serializer, version="v1"))
