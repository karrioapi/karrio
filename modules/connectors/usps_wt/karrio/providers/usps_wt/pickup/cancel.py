from typing import Tuple, List
from karrio.schemas.usps_wt.carrier_pickup_cancel_request import (
    CarrierPickupCancelRequest,
)
from karrio.core.utils import Serializable, SF
from karrio.core.models import PickupCancelRequest, ConfirmationDetails, Message

from karrio.providers.usps_wt.error import parse_error_response
from karrio.providers.usps_wt.utils import Settings
import karrio.lib as lib


def parse_pickup_cancel_response(
    _response: lib.Deserializable[dict],
    settings: Settings,
) -> Tuple[ConfirmationDetails, List[Message]]:
    response = _response.deserialize()
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
        PASSWORD=settings.password,
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
