from typing import Tuple, List
from purplship.core.utils import Serializable
from purplship.core.models import (
    ShipmentRequest,
    ShipmentDetails,
    Message
)

from purplship.providers.boxknight.error import parse_error_response
from purplship.providers.boxknight.utils import Settings


def parse_shipment_response(response: dict, settings: Settings) -> Tuple[ShipmentDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    details = None

    return details, errors


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable:
    request = None

    return Serializable(request)
