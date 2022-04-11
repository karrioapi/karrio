from typing import List, Tuple
from karrio.core.models import ShipmentCancelRequest, ConfirmationDetails, Message
from karrio.core.utils import Serializable
from karrio.providers.easypost.error import parse_error_response
from karrio.providers.easypost.utils import Settings


def parse_shipment_cancel_response(
    responses: List[Tuple[str, dict]], settings: Settings
) -> Tuple[ConfirmationDetails, List[Message]]:
    statuses: List[str] = [response.get("status") for _, response in responses]
    errors = [
        parse_error_response(response, settings)
        for _, response in responses
        if "error" in response
    ]
    messages = [
        Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code="rejected",
            message=f"shipment {shipment.get('id')} refund was rejected",
        )
        for _, shipment in responses
        if shipment.get("status") == "rejected"
    ]

    details = ConfirmationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success=any(status != "rejected" for status in statuses),
        operation="cancel shipment",
    )

    return details, [*errors, *messages]


def shipment_cancel_request(payload: ShipmentCancelRequest, _) -> Serializable:
    request = (
        payload.options.shipment_identifiers
        if "shipment_identifiers" in (payload.options or {})
        else [payload.shipment_identifier]
    )

    return Serializable(request)
