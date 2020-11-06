from typing import List, Tuple
from pycanpar.CanparAddonsService import (
    cancelPickup,
    CancelPickupRq,
)
from purplship.core.models import (
    PickupCancelRequest,
    ConfirmationDetails,
    Message,
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
    errors = parse_error_response(response, settings)
    success = len(errors) == 0
    confirmation: ConfirmationDetails = ConfirmationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success=success,
        operation="Cancel Pickup",
    ) if success else None

    return confirmation, errors


def cancel_pickup_request(payload: PickupCancelRequest, settings: Settings) -> Serializable[Envelope]:

    request = create_envelope(
        body_content=cancelPickup(
            request=CancelPickupRq(
                id=int(payload.confirmation_number),
                password=settings.password,
                user_id=settings.username
            )
        )
    )

    return Serializable(request, default_request_serializer)
