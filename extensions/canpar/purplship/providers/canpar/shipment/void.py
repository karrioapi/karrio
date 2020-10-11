from typing import List, Tuple
from pycanpar.CanshipBusinessService import (
    voidShipment,
    VoidShipmentRq
)
from purplship.core.models import (
    VoidShipmentRequest,
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
from purplship.providers.canpar.utils import Settings, default_request_serializer


def parse_void_shipment_response(response: Element, settings: Settings) -> Tuple[ConfirmationDetails, List[Message]]:
    confirmation: ConfirmationDetails = None

    return confirmation, parse_error_response(response, settings)


def void_shipment_request(payload: VoidShipmentRequest, settings: Settings) -> Serializable[Envelope]:

    request = create_envelope(
        body_content=voidShipment(
            request=VoidShipmentRq(
                id=payload.tracking_number,
                password=settings.password,
                user_id=settings.user_id
            )
        )
    )

    return Serializable(request, default_request_serializer)
