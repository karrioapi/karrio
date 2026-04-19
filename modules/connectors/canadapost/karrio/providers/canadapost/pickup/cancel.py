import karrio.lib as lib
from karrio.core.models import (
    ConfirmationDetails,
    Message,
    PickupCancelRequest,
)
from karrio.core.utils import Element, Serializable
from karrio.providers.canadapost.error import parse_error_response
from karrio.providers.canadapost.utils import Settings


def parse_pickup_cancel_response(
    _response: lib.Deserializable[Element], settings: Settings
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
        if len(errors) == 0
        else None
    )

    return cancellation, errors


def pickup_cancel_request(payload: PickupCancelRequest, _) -> Serializable:
    return Serializable(payload.confirmation_number)
