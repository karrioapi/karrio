from typing import Tuple, List
from karrio.core.utils import Serializable
from karrio.core.models import (
    ShipmentCancelRequest,
    ConfirmationDetails,
    Message
)

from karrio.providers.boxknight.error import parse_error_response
from karrio.providers.boxknight.utils import Settings


def parse_shipment_cancel_response(response: dict, settings: Settings) -> Tuple[ConfirmationDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    details = None

    return details, errors


def shipment_cancel_request(payload: ShipmentCancelRequest, _) -> Serializable:
    request = payload.shipment_identifier

    return Serializable(request)
