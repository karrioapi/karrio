from typing import Tuple, List
from usps_lib.evs_cancel_request import eVSCancelRequest
from usps_lib.evs_cancel_response import eVSCancelResponse
from karrio.core.utils import Serializable, Element, XP
from karrio.core.models import (
    ShipmentCancelRequest,
    ConfirmationDetails,
    Message
)

from karrio.providers.usps.error import parse_error_response
from karrio.providers.usps.utils import Settings


def parse_shipment_cancel_response(response: Element, settings: Settings) -> Tuple[ConfirmationDetails, List[Message]]:
    errors: List[Message] = parse_error_response(response, settings)
    cancel_response = XP.to_object(eVSCancelResponse, response)

    if cancel_response.Status != "Cancelled":
        errors.append(Message(
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            message=cancel_response.Reason,
            code=cancel_response.Status
        ))

    details = (
        ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            operation="Shipment Cancel",
            success=True,
        )
        if not any(errors) else None
    )

    return details, errors


def shipment_cancel_request(payload: ShipmentCancelRequest, settings: Settings) -> Serializable:

    request = eVSCancelRequest(
        USERID=settings.username,
        BarcodeNumber=payload.shipment_identifier
    )

    return Serializable(request, XP.export)
