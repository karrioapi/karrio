from typing import List, Tuple
from karrio.core.models import ShipmentCancelRequest, ConfirmationDetails, Message
from karrio.core.utils import Serializable
from karrio.providers.easypost.error import parse_error_response
from karrio.providers.easypost.utils import Settings


def parse_shipment_cancel_response(
    response: dict, settings: Settings
) -> Tuple[ConfirmationDetails, List[Message]]:
    status = response.get("status")
    errors = [parse_error_response(response, settings)] if "error" in response else []

    details = ConfirmationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success=status != "rejected",
        operation="cancel shipment",
    )

    return details, errors


def shipment_cancel_request(payload: ShipmentCancelRequest, _) -> Serializable:
    return Serializable(payload.shipment_identifier)
