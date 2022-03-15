from typing import Tuple, List
from karrio.core.utils import Serializable
from karrio.core.models import (
    PickupCancelRequest,
    ConfirmationDetails,
    Message
)

from karrio.providers.boxknight.error import parse_error_response
from karrio.providers.boxknight.utils import Settings


def parse_pickup_cancel_response(response: dict, settings: Settings) -> Tuple[ConfirmationDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    details = None

    return details, errors


def pickup_cancel_request(payload: PickupCancelRequest, _) -> Serializable:

    request = payload.confirmation_number

    return Serializable(request)
