from typing import List, Tuple
from karrio.schemas.freightcom.shipment_cancel_request import (
    ShipmentCancelRequestType,
    Freightcom,
    OrderType,
)
from karrio.core.models import ShipmentCancelRequest, ConfirmationDetails, Message
from karrio.core.utils import (
    Element,
    Serializable,
)
from karrio.providers.freightcom.error import parse_error_response
from karrio.providers.freightcom.utils import Settings, standard_request_serializer
import karrio.lib as lib


def parse_shipment_cancel_reply(
    _response: lib.Deserializable[Element],
    settings: Settings,
) -> Tuple[ConfirmationDetails, List[Message]]:
    response = _response.deserialize()
    errors = parse_error_response(response, settings)
    success = len(errors) == 0
    confirmation: ConfirmationDetails = (
        ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=success,
            operation="Cancel Shipment",
        )
        if success
        else None
    )

    return confirmation, errors


def shipment_cancel_request(
    payload: ShipmentCancelRequest, settings: Settings
) -> Serializable:
    request = Freightcom(
        username=settings.username,
        password=settings.password,
        version="3.1.0",
        ShipmentCancelRequest=ShipmentCancelRequestType(
            Order=OrderType(orderId=payload.shipment_identifier)
        ),
    )

    return Serializable(request, standard_request_serializer)
