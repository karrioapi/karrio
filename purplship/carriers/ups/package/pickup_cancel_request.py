from pyups.pickup_web_service_schema import (
    PickupCancelRequest
)
from purplship.core.utils.xml import Element
from purplship.core.models import PickupDetails, PickupCancellationRequest
from purplship.carriers.ups import Settings


def parse_pickup_cancel_response(response: Element, settings: Settings) -> PickupDetails:
    pass


def pickup_cancel_request(payload: PickupCancellationRequest, settings: Settings) -> PickupCancelRequest:
    return PickupCancelRequest(
        Request=None,
        CancelBy=None,
        PRN=None
    )
