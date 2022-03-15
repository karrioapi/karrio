from typing import Tuple, List
from functools import partial
from purolator_lib.pickup_service_1_2_1 import (
    VoidPickUpRequest,
    RequestContext,
)
from karrio.core.models import (
    PickupCancelRequest,
    ConfirmationDetails,
    Message,
)
from karrio.core.utils import Serializable, create_envelope, Envelope, Element
from karrio.providers.purolator.error import parse_error_response
from karrio.providers.purolator.utils import Settings, standard_request_serializer


def parse_pickup_cancel_response(
    response: Element, settings: Settings
) -> Tuple[ConfirmationDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    cancellation = (
        ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=True,
            operation="Cancel Pickup",
        )
        if not any(errors) else None
    )

    return cancellation, errors


def pickup_cancel_request(
    payload: PickupCancelRequest, settings: Settings
) -> Serializable[Envelope]:

    request = create_envelope(
        header_content=RequestContext(
            Version="1.2",
            Language=settings.language,
            GroupID="",
            RequestReference="",
            UserToken=settings.user_token,
        ),
        body_content=VoidPickUpRequest(
            PickUpConfirmationNumber=payload.confirmation_number
        ),
    )

    return Serializable(request, partial(standard_request_serializer, version="v1"))
