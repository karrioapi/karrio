from typing import Tuple, List
from boxknight_lib.orders import (
    OrderRequest,
    Address,
    Recipient,
)
from purplship.core.utils import Serializable, SF
from purplship.core.models import (
    ShipmentRequest,
    ShipmentDetails,
    Message
)

from purplship.providers.boxknight.units import Service, Option
from purplship.providers.boxknight.error import parse_error_response
from purplship.providers.boxknight.utils import Settings


def parse_shipment_response(response: dict, settings: Settings) -> Tuple[ShipmentDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    details = None

    return details, errors


def shipment_request(payload: ShipmentRequest, _) -> Serializable:

    request = OrderRequest(
        packageCount=len(payload.parcels),
        signatureRequired=payload.options.get('signature_required', False),
        recipient=Recipient(
            name=payload.recipient.person_name,
            phone=payload.recipient.phone_number,
            notes=None,
            email=payload.recipient.email
        ),
        recipientAddress=Address(
            street=SF.concat_str(payload.recipient.address_line1, payload.recipient.address_line2, join=True),
            city=payload.recipient.city,
            province=payload.recipient.state_code,
            country=payload.recipient.country_code,
            postalCode=payload.recipient.postal_code,
            unit=None
        ),
        originAddress=Address(
            street=SF.concat_str(payload.shipper.address_line1, payload.shipper.address_line2, join=True),
            city=payload.shipper.city,
            province=payload.shipper.state_code,
            country=payload.shipper.country_code,
            postalCode=payload.shipper.postal_code,
            unit=None
        ),
        service=Service[payload.service].value,
        notes=None,
        refNumber=payload.reference,
        completeAfter=None,
        completeBefore=None,
        merchantDisplayName=payload.shipper.company_name
    )

    return Serializable(request)
