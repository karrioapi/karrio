from typing import List, Tuple
from karrio.schemas.dhl_poland.services import (
    deleteShipment,
    DeleteShipmentRequest,
)
from karrio.core.models import ShipmentCancelRequest, ConfirmationDetails, Message
from karrio.core.utils import (
    create_envelope,
    Envelope,
    Element,
    Serializable,
)
from karrio.providers.dhl_poland.error import parse_error_response
from karrio.providers.dhl_poland.utils import Settings
import karrio.lib as lib


def parse_shipment_cancel_response(
    _response: lib.Deserializable[Element], settings: Settings
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
    request = create_envelope(
        body_content=deleteShipment(
            authData=settings.auth_data,
            shipment=DeleteShipmentRequest(
                shipmentIdentificationNumber=payload.shipment_identifier
            ),
        )
    )

    return Serializable(
        request,
        lambda request: settings.serialize(
            request, "deleteShipment", settings.server_url
        ),
    )
