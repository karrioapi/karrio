from typing import List, Tuple
from ics_courier_lib.services import (
    VoidPackages,
    Authenticate,
    ArrayOfString,
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
from purplship.providers.ics_courier.error import parse_error_response
from purplship.providers.ics_courier.utils import Settings


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
        body_content=VoidPackages(
            AuthenicateAccount=Authenticate(
                AccountID=settings.account_id,
                Password=settings.password,
            ),
            Packages=ArrayOfString(
                string=[payload.shipment_identifier]
            ),
        )
    )

    return Serializable(request, Settings.serialize)
