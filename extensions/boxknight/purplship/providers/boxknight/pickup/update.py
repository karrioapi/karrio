from typing import Tuple, List
from purplship.core.utils import Serializable
from purplship.core.models import (
    PickupUpdateRequest,
    PickupDetails,
    Message
)

from purplship.providers.boxknight.error import parse_error_response
from purplship.providers.boxknight.utils import Settings


def parse_pickup_update_response(response: dict, settings: Settings) -> Tuple[PickupDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    details = None

    return details, errors


def pickup_update_request(payload: PickupUpdateRequest, settings: Settings) -> Serializable:
    request = None

    return Serializable(request)
