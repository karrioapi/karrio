from typing import List, Tuple
from karrio.core.models import ShipmentCancelRequest, ConfirmationDetails, Message
from karrio.core.utils import (
    Serializable,
)
from karrio.providers.amazon_shipping.error import parse_error_response
from karrio.providers.amazon_shipping.utils import Settings
import karrio.lib as lib


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: Settings,
) -> Tuple[ConfirmationDetails, List[Message]]:
    response = _response.deserialize()
    errors = [
        parse_error_response(data, settings) for data in response.get("errors", [])
    ]
    details = ConfirmationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success="errors" not in response,
        operation="cancel shipment",
    )

    return details, errors


def shipment_cancel_request(payload: ShipmentCancelRequest, _) -> Serializable:
    return Serializable(payload.shipment_identifier)
