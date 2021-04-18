from typing import List, Tuple
from fedex_lib.ship_service_v25 import (
    DeleteShipmentRequest,
    TrackingId,
    TransactionDetail,
    VersionId,
    DeletionControlType,
    TrackingIdType,
)
from purplship.core.models import (
    ShipmentCancelRequest,
    ConfirmationDetails,
    Message
)
from purplship.core.utils import (
    Envelope,
    Element,
    Serializable,
    create_envelope,
)
from purplship.providers.fedex.error import parse_error_response
from purplship.providers.fedex.utils import Settings, default_request_serializer


def parse_shipment_cancel_response(response: Element, settings: Settings) -> Tuple[ConfirmationDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    success = len(errors) == 0
    confirmation: ConfirmationDetails = ConfirmationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success=success,
        operation="Cancel Shipment",
    ) if success else None

    return confirmation, errors


def shipment_cancel_request(payload: ShipmentCancelRequest, settings: Settings) -> Serializable[Envelope]:
    tracking_type = next(
        (t for t in list(TrackingIdType) if t.name.lower() in payload.service),
        TrackingIdType.EXPRESS
    ).value
    deletion_type = DeletionControlType[
        payload.options.get('deletion_type', 'DELETE_ALL_PACKAGES')
    ].value

    request = create_envelope(
        body_content=DeleteShipmentRequest(
            WebAuthenticationDetail=settings.webAuthenticationDetail,
            ClientDetail=settings.clientDetail,
            TransactionDetail=TransactionDetail(CustomerTransactionId="Delete Shipment"),
            Version=VersionId(ServiceId="ship", Major=23, Intermediate=0, Minor=0),
            ShipTimestamp=None,
            TrackingId=TrackingId(
                TrackingIdType=tracking_type,
                FormId=None,
                UspsApplicationId=None,
                TrackingNumber=payload.shipment_identifier
            ),
            DeletionControl=deletion_type
        )
    )

    return Serializable(
        request,
        default_request_serializer('v23', 'xmlns:v23="http://fedex.com/ws/ship/v23"')
    )
