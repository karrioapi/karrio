from typing import Tuple, List
from purplship.core.utils import Serializable
from purplship.core.models import (
    PickupRequest,
    PickupDetails,
    Message
)

from purplship.providers.boxknight.error import parse_error_response
from purplship.providers.boxknight.utils import Settings


def parse_pickup_response(response: dict, settings: Settings) -> Tuple[PickupDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    details = None

    return details, errors


def pickup_request(payload: PickupRequest, settings: Settings) -> Serializable:
    request = None

    return Serializable(request)
