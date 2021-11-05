from typing import Tuple, List
from boxknight_lib.pickups import PickupUpdateRequest as BoxKnightPickupUpdateRequest
from purplship.core.utils import Serializable
from purplship.core.models import (
    ShipmentDetails,
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


def pickup_update_request(payload: PickupUpdateRequest, _) -> Serializable:
    shipments: List[ShipmentDetails] = payload.options.get('shipments', [])

    request = BoxKnightPickupUpdateRequest(
        orderIds=[shipment.shipment_identifier for shipment in shipments]
    )

    return Serializable(request)
