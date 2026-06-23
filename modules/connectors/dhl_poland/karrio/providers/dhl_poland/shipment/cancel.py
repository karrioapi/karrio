import karrio.lib as lib
from karrio.core.models import ConfirmationDetails, Message, ShipmentCancelRequest
from karrio.core.utils import (
    Element,
    Serializable,
    create_envelope,
)
from karrio.providers.dhl_poland.error import parse_error_response
from karrio.providers.dhl_poland.utils import Settings
from karrio.schemas.dhl_poland.services import (
    DeleteShipmentRequest,
    deleteShipment,
)


def parse_shipment_cancel_response(
    _response: lib.Deserializable[Element], settings: Settings
) -> tuple[ConfirmationDetails, list[Message]]:
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


def shipment_cancel_request(payload: ShipmentCancelRequest, settings: Settings) -> Serializable:
    request = create_envelope(
        body_content=deleteShipment(
            authData=settings.auth_data,
            shipment=DeleteShipmentRequest(shipmentIdentificationNumber=payload.shipment_identifier),
        )
    )

    return Serializable(
        request,
        lambda request: settings.serialize(request, "deleteShipment", settings.server_url),
    )
