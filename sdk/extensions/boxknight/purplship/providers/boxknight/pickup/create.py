from typing import Tuple, List
from boxknight_lib.pickups import (
    PickupRequest as BoxKnightPickupRequest,
    PickupRequestRecipientAddress,
    Recipient,
)
from purplship.core.utils import Serializable, SF, DF
from purplship.core.models import (
    ShipmentDetails,
    PickupRequest,
    PickupDetails,
    Message,
)

from purplship.providers.boxknight.error import parse_error_response
from purplship.providers.boxknight.utils import Settings


def parse_pickup_response(response: dict, settings: Settings) -> Tuple[PickupDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    details = None

    return details, errors


def pickup_request(payload: PickupRequest, _) -> Serializable:
    shipments: List[ShipmentDetails] = payload.options.get('shipments', [])
    after = DF.date(f"{payload.pickup_date} {payload.ready_time}", current_format="%Y-%m-%d %H:%M")
    before = DF.date(f"{payload.pickup_date} {payload.ready_time}", current_format="%Y-%m-%d %H:%M")

    request = BoxKnightPickupRequest(
        packageCount=len(payload.parcels),
        recipient=Recipient(
            name=payload.address.person_name,
            phone=payload.address.phone_number,
            notes=None,
            email=payload.address.email,
        ),
        recipientAddress=PickupRequestRecipientAddress(
            street=SF.concat_str(payload.address.address_line1, payload.address.address_line2, join=True),
            city=payload.address.city,
            province=payload.address.state_code,
            country=payload.address.country_code,
            postalCode=payload.address.postal_code,
            unit=None
        ),
        notes=payload.instruction,
        completeAfter=int(after.timestamp() * 1000.0),
        completeBefore=int(before.timestamp() * 1000.0),
        orderIds=[shipment.shipment_identifier for shipment in shipments],
    )

    return Serializable(request)
