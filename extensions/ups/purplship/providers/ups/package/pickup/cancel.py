from typing import List, Tuple
from pyups.pickup_web_service_schema import (
    PickupCancelRequest,
    CodeDescriptionType,
    RequestType,
)
from purplship.core.utils import Envelope, Element, create_envelope, Serializable, build
from purplship.core.models import (
    PickupCancellationRequest,
    ConfirmationDetails,
    Message,
)
from purplship.providers.ups.utils import Settings, default_request_serializer
from purplship.providers.ups.error import parse_error_response


def parse_cancel_pickup_response(
    response: Element, settings: Settings
) -> Tuple[ConfirmationDetails, List[Message]]:
    status = build(
        CodeDescriptionType,
        next(
            iter(response.xpath(".//*[local-name() = $name]", name="ResponseStatus")),
            None,
        ),
    )
    success = status is not None and status.Code == "1"
    cancellation = (
        ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=success,
        )
        if success
        else None
    )

    return cancellation, parse_error_response(response, settings)


def cancel_pickup_request(
    payload: PickupCancellationRequest, settings: Settings
) -> Serializable[Envelope]:

    request = create_envelope(
        header_content=settings.Security,
        body_content=PickupCancelRequest(
            Request=RequestType(), CancelBy="02", PRN=payload.confirmation_number
        ),
    )

    return Serializable(
        request,
        default_request_serializer(
            "v11", 'xmlns:v11="http://www.ups.com/XMLSchema/XOLTWS/Pickup/v1.1"'
        ),
    )
