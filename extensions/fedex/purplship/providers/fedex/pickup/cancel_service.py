from typing import Tuple, List
from pyfedex.pickup_service_v20 import (
    CancelPickupRequest,
    TransactionDetail,
    VersionId,
    CarrierCodeType
)
from purplship.core.models import PickupCancellationRequest, ConfirmationDetails, Message
from purplship.core.utils import Serializable, export, create_envelope, apply_namespaceprefix, Envelope, Element
from purplship.providers.fedex.error import parse_error_response
from purplship.providers.fedex.utils import Settings


def parse_cancel_pickup_reply(response: Element, settings: Settings) -> Tuple[ConfirmationDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    cancellation = ConfirmationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success=True
    ) if len(errors) == 0 else None

    return cancellation, errors


def cancel_pickup_request(payload: PickupCancellationRequest, settings: Settings) -> Serializable[CancelPickupRequest]:

    request = CancelPickupRequest(
        WebAuthenticationDetail=settings.webAuthenticationDetail,
        ClientDetail=settings.clientDetail,
        TransactionDetail=TransactionDetail(CustomerTransactionId="FTC"),
        Version=VersionId(ServiceId="disp", Major=17, Intermediate=0, Minor=0),
        CarrierCode=[CarrierCodeType.FDXE.value],
        PickupConfirmationNumber=payload.confirmation_number,
        ScheduledDate=payload.pickup_date,
        EndDate=None,
        Location=None,
        Remarks=None,
        ShippingChargesPayment=None,
        Reason=payload.reason,
        ContactName=payload.address.person_name,
        PhoneNumber=payload.address.phone_number,
        PhoneExtension=None
    )

    return Serializable(request, _request_serializer)


def _request_serializer(request: CancelPickupRequest) -> str:
    envelope: Envelope = create_envelope(body_content=request)
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "v17")

    return export(
        envelope,
        namespacedef_='xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v17="http://fedex.com/ws/pickup/v17"'
    )
