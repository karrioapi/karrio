from typing import Tuple, List
from fedex_lib.pickup_service_v20 import (
    CancelPickupRequest,
    TransactionDetail,
    VersionId,
    CarrierCodeType,
    CancelPickupReply,
    NotificationSeverityType,
)
from purplship.core.models import (
    PickupCancelRequest,
    ConfirmationDetails,
    Message,
)
from purplship.core.utils import (
    Serializable,
    create_envelope,
    apply_namespaceprefix,
    Envelope,
    Element,
    XP,
)
from purplship.providers.fedex.error import parse_error_response
from purplship.providers.fedex.utils import Settings


def parse_pickup_cancel_response(
    response: Element, settings: Settings
) -> Tuple[ConfirmationDetails, List[Message]]:
    reply = XP.build(
        CancelPickupReply,
        next(
            iter(
                response.xpath(".//*[local-name() = $name]", name="CancelPickupReply")
            ),
            None,
        ),
    )
    cancellation = ConfirmationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success=reply.HighestSeverity == NotificationSeverityType.SUCCESS.value,
        operation="Cancel Pickup",
    )

    return cancellation, parse_error_response(response, settings)


def pickup_cancel_request(
    payload: PickupCancelRequest, settings: Settings
) -> Serializable[CancelPickupRequest]:

    request = CancelPickupRequest(
        WebAuthenticationDetail=settings.webAuthenticationDetail,
        ClientDetail=settings.clientDetail,
        TransactionDetail=TransactionDetail(CustomerTransactionId="FTC"),
        Version=VersionId(ServiceId="disp", Major=17, Intermediate=0, Minor=0),
        CarrierCode=CarrierCodeType.FDXE.value,
        PickupConfirmationNumber=payload.confirmation_number,
        ScheduledDate=payload.pickup_date,
        EndDate=None,
        Location=None,
        Remarks=None,
        ShippingChargesPayment=None,
        Reason=payload.reason,
        ContactName=(
            payload.address.person_name if payload.address is not None else None
        ),
        PhoneNumber=(
            payload.address.phone_number if payload.address is not None else None
        ),
        PhoneExtension=None,
    )

    return Serializable(request, _request_serializer)


def _request_serializer(request: CancelPickupRequest) -> str:
    envelope: Envelope = create_envelope(body_content=request)
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "v17")

    return XP.export(
        envelope,
        namespacedef_='xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v17="http://fedex.com/ws/pickup/v17"',
    )
