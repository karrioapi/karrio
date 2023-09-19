from typing import Tuple, List
from karrio.core.utils import Serializable
from karrio.core.models import ShipmentCancelRequest, ConfirmationDetails, Message

from karrio.providers.dicom.error import parse_error_response
from karrio.providers.dicom.utils import Settings
import karrio.lib as lib


def parse_shipment_cancel_response(
    response: lib.Deserializable[dict],
    settings: Settings,
) -> Tuple[ConfirmationDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    details = (
        ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            operation="Shipment Cancel",
            success=True,
        )
        if not any(errors)
        else None
    )

    return details, errors


def shipment_cancel_request(payload: ShipmentCancelRequest, _) -> Serializable:
    request = payload.shipment_identifier

    return Serializable(request)
