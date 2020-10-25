from typing import List, Tuple
from purplship.core.models import (
    ShipmentCancelRequest,
    ConfirmationDetails,
    Message
)
from purplship.core.utils import (
    Element,
    Serializable,
)
from purplship.providers.canadapost.error import parse_error_response
from purplship.providers.canadapost.utils import Settings


def parse_void_shipment_response(response: Element, settings: Settings) -> Tuple[ConfirmationDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    success = len(errors) == 0
    confirmation: ConfirmationDetails = ConfirmationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success=success,
        operation="Cancel Shipment",
    ) if success else None

    return confirmation, errors


def void_shipment_request(payload: ShipmentCancelRequest, _) -> Serializable[str]:
    return Serializable(payload.shipment_identifier)
