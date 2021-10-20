from typing import List, Tuple
from canpar_lib.CanshipBusinessService import (
    voidShipment,
    VoidShipmentRq,
)
from purplship.core.models import (
    ShipmentCancelRequest,
    ConfirmationDetails,
    Message
)
from purplship.core.utils import (
    create_envelope,
    Envelope,
    Element,
    Serializable,
)
from purplship.providers.canpar.error import parse_error_response
from purplship.providers.canpar.utils import Settings


def parse_shipment_cancel_response(response: Element, settings: Settings) -> Tuple[ConfirmationDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    success = len(errors) == 0
    confirmation: ConfirmationDetails = ConfirmationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success=success,
        operation="Cancel Shipment"
    ) if success else None

    return confirmation, errors


def shipment_cancel_request(payload: ShipmentCancelRequest, settings: Settings) -> Serializable[Envelope]:

    request = create_envelope(
        body_content=voidShipment(
            request=VoidShipmentRq(
                id=int(payload.shipment_identifier),
                password=settings.password,
                user_id=settings.username
            )
        )
    )

    return Serializable(request, Settings.serialize)
