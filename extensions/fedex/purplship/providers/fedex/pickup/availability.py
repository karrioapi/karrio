from datetime import datetime
from fedex_lib.pickup_service_v20 import (
    PickupAvailabilityRequest,
    TransactionDetail,
    VersionId,
    Address,
    CarrierCodeType,
    PickupRequestType,
    AssociatedAccount,
    AssociatedAccountNumberType,
)
from purplship.core.models import PickupRequest
from purplship.core.utils import (
    Serializable,
    create_envelope,
    apply_namespaceprefix,
    Envelope,
    SF,
    XP,
    DF,
)
from purplship.providers.fedex.utils import Settings


def pickup_availability_request(
    payload: PickupRequest, settings: Settings
) -> Serializable[PickupAvailabilityRequest]:
    same_day = DF.date(payload.pickup_date).date() == datetime.today().date()

    request = PickupAvailabilityRequest(
        WebAuthenticationDetail=settings.webAuthenticationDetail,
        ClientDetail=settings.clientDetail,
        TransactionDetail=TransactionDetail(CustomerTransactionId="FTC"),
        Version=VersionId(ServiceId="disp", Major=17, Intermediate=0, Minor=0),
        PickupType=None,
        AccountNumber=AssociatedAccount(
            Type=AssociatedAccountNumberType.FEDEX_EXPRESS.value,
            AccountNumber=settings.account_number,
        ),
        PickupAddress=Address(
            StreetLines=SF.concat_str(
                payload.address.address_line1, payload.address.address_line2
            ),
            City=payload.address.city,
            StateOrProvinceCode=payload.address.state_code,
            PostalCode=payload.address.postal_code,
            CountryCode=payload.address.country_code,
            Residential=payload.address.residential,
        ),
        PickupRequestType=[
            (
                PickupRequestType.SAME_DAY if same_day else PickupRequestType.FUTURE_DAY
            ).value
        ],
        DispatchDate=payload.pickup_date,
        NumberOfBusinessDays=None,
        PackageReadyTime=f"{payload.ready_time}:00",
        CustomerCloseTime=f"{payload.closing_time}:00",
        Carriers=[CarrierCodeType.FDXE.value],
        ShipmentAttributes=None,
        PackageDetails=None,
    )

    return Serializable(request, _request_serializer)


def _request_serializer(request: PickupAvailabilityRequest) -> str:
    envelope: Envelope = create_envelope(body_content=request)
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "v17")

    return XP.export(
        envelope,
        namespacedef_='xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v17="http://fedex.com/ws/pickup/v17"',
    )
