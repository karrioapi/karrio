from pyups.freight_pickup_web_service_schema import (
    FreightCancelPickupRequest
)
from purplship.core.utils.xml import Element
from purplship.core.models import PickupDetails, PickupCancellationRequest
from purplship.carriers.ups import Settings


def parse_cancel_pickup_response(response: Element, settings: Settings) -> PickupDetails:
    pass


def freight_cancel_pickup(payload: PickupCancellationRequest, settings: Settings) -> FreightCancelPickupRequest:
    return FreightCancelPickupRequest(
        Request=None,
        PickupRequestConfirmationNumber=None
    )
