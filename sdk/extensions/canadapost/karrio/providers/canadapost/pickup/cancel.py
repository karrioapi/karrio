from typing import Tuple, List
from karrio.core.models import (
    PickupCancelRequest,
    Message,
    ConfirmationDetails,
)
from karrio.core.utils import Serializable, Element
from karrio.providers.canadapost.error import parse_error_response
from karrio.providers.canadapost.utils import Settings


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
        if len(errors) == 0
        else None
    )

    return cancellation, errors


def pickup_cancel_request(payload: PickupCancelRequest, _) -> Serializable[str]:
    return Serializable(payload.confirmation_number)
