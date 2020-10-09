from typing import List, Tuple
from pycanpar.CanparAddonsService import (
    cancelPickup,
    CancelPickupRq
)
from purplship.core.models import (
    PickupCancellationRequest,
    ConfirmationDetails,
    Message
)
from purplship.core.utils import (
    create_envelope,
    Envelope,
    Element,
    Serializable
)
from purplship.providers.canpar.error import parse_error_response
from purplship.providers.canpar.utils import Settings, default_request_serializer


def parse_cancel_pickup_response(response: Element, settings: Settings) -> Tuple[ConfirmationDetails, List[Message]]:
    confirmation: ConfirmationDetails = None

    return confirmation, parse_error_response(response, settings)


def cancel_pickup_request(payload: PickupCancellationRequest, settings: Settings) -> Serializable[Envelope]:

    request = create_envelope(
        body_content=cancelPickup(
            request=CancelPickupRq(
                id=payload.confirmation_number,
                password=settings.password,
                user_id=settings.user_id
            )
        )
    )

    return Serializable(request, default_request_serializer)
