import karrio.lib as lib
from typing import List, Tuple
from karrio.schemas.canpar.CanparAddonsService import (
    cancelPickup,
    CancelPickupRq,
)
from karrio.core.models import (
    PickupCancelRequest,
    ConfirmationDetails,
    Message,
)
from karrio.core.utils import create_envelope, Element, Serializable
from karrio.providers.canpar.error import parse_error_response
from karrio.providers.canpar.utils import Settings


def parse_pickup_cancel_response(
    _response: lib.Deserializable[Element],
    settings: Settings,
) -> Tuple[ConfirmationDetails, List[Message]]:
    response = _response.deserialize()
    errors = parse_error_response(response, settings)
    success = len(errors) == 0
    confirmation: ConfirmationDetails = (
        ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=success,
            operation="Cancel Pickup",
        )
        if success
        else None
    )

    return confirmation, errors


def pickup_cancel_request(
    payload: PickupCancelRequest, settings: Settings
) -> Serializable:
    request = create_envelope(
        body_content=cancelPickup(
            request=CancelPickupRq(
                id=int(payload.confirmation_number),
                password=settings.password,
                user_id=settings.username,
            )
        )
    )

    return Serializable(request, Settings.serialize)
