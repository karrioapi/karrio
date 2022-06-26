from typing import Tuple, List
from usps_lib.carrier_pickup_cancel_request import CarrierPickupCancelRequest
from karrio.core.utils import Serializable, SF
from karrio.core.models import PickupCancelRequest, ConfirmationDetails, Message

from karrio.providers.usps_international.error import parse_error_response
from karrio.providers.usps_international.utils import Settings


def parse_pickup_cancel_response(
    response: dict, settings: Settings
) -> Tuple[ConfirmationDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    details = (
        ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=True,
            operation="Pickup Cancel",
        )
        if not any(errors)
        else None
    )

    return details, errors


def pickup_cancel_request(
    payload: PickupCancelRequest, settings: Settings
) -> Serializable:

    request = CarrierPickupCancelRequest(
        UserID=settings.username,
        FirmName=payload.address.company_name,
        SuiteOrApt=payload.address.address_line1,
        Address2=SF.concat_str(
            payload.address.address_line1, payload.address.address_line2, join=True
        ),
        Urbanization=None,
        City=payload.address.city,
        State=payload.address.state_code,
        ZIP5=payload.address.postal_code,
        ZIP4=None,
        ConfirmationNumber=payload.confirmation_number,
    )

    return Serializable(request)
