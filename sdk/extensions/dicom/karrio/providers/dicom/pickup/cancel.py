from typing import Tuple, List
from karrio.core.utils import Serializable
from karrio.core.models import PickupCancelRequest, ConfirmationDetails, Message

from karrio.providers.dicom.error import parse_error_response
from karrio.providers.dicom.utils import Settings
import karrio.lib as lib


def parse_pickup_cancel_response(
    _response: lib.Deserializable[dict],
    settings: Settings,
) -> Tuple[ConfirmationDetails, List[Message]]:
    response = _response.deserialize()
    errors = parse_error_response(response, settings)
    details = (
        ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=True,
            operation="Pickup Cancel",
        )
        if not any(errors)
        else None
    )

    return details, errors


def pickup_cancel_request(payload: PickupCancelRequest, _) -> Serializable:
    request = payload.confirmation_number

    return Serializable(request)
