from datetime import datetime
from typing import List, Tuple
from functools import partial
from fedex_lib.pickup_service_v20 import (
    PickupAvailabilityReply,
    CreatePickupRequest,
    TransactionDetail,
    VersionId,
    PickupOriginDetail,
    ContactAndAddress,
    AssociatedAccount,
    AssociatedAccountNumberType,
    Address,
    Contact,
    Weight,
    WeightUnits,
    CarrierCodeType,
    PickupRequestType,
    CreatePickupReply,
    NotificationSeverityType,
)
from purplship.core.models import PickupRequest, PickupDetails, Message
from purplship.core.units import Packages
from purplship.core.utils import (
    Serializable,
    create_envelope,
    apply_namespaceprefix,
    Envelope,
    Element,
    Pipeline,
    Job,
    SF,
    DF,
    XP,
)
from purplship.providers.fedex.pickup.availability import pickup_availability_request
from purplship.providers.fedex.utils import Settings
from purplship.providers.fedex.units import PackagePresets
from purplship.providers.fedex.error import parse_error_response


def parse_pickup_response(
    response: Element, settings: Settings
) -> Tuple[PickupDetails, List[Message]]:
    reply = XP.build(
        CreatePickupReply,
        next(
            iter(
                response.xpath(".//*[local-name() = $name]", name="CreatePickupReply")
            ),
            None,
        ),
    )
    pickup = (
        _extract_pickup_details(reply, settings)
        if reply.HighestSeverity == NotificationSeverityType.SUCCESS.value
        else None
    )
    return pickup, parse_error_response(response, settings)


def _extract_pickup_details(
    reply: CreatePickupReply, settings: Settings
) -> PickupDetails:
    return PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=reply.PickupConfirmationNumber,
    )


def pickup_request(
    payload: PickupRequest, settings: Settings
) -> Serializable[Pipeline]:
    """
    Create a pickup request
    Steps
        1 - get availability
        2 - create pickup
    :param payload: PickupRequest
    :param settings: Settings
    :return: Serializable[Pipeline]
    """
    request: Pipeline = Pipeline(
        get_availability=lambda *_: _get_availability(
            payload=payload, settings=settings
        ),
        create_pickup=partial(_create_pickup, payload=payload, settings=settings),
    )
    return Serializable(request)


def _pickup_request(
    payload: PickupRequest, settings: Settings
) -> Serializable[CreatePickupRequest]:
    same_day = DF.date(payload.pickup_date).date() == datetime.today().date()
    packages = Packages(payload.parcels, PackagePresets, required=["weight"])

    request = CreatePickupRequest(
        WebAuthenticationDetail=settings.webAuthenticationDetail,
        ClientDetail=settings.clientDetail,
        TransactionDetail=TransactionDetail(CustomerTransactionId="FTC"),
        Version=VersionId(ServiceId="disp", Major=17, Intermediate=0, Minor=0),
        AssociatedAccountNumber=AssociatedAccount(
            Type=AssociatedAccountNumberType.FEDEX_EXPRESS.value,
            AccountNumber=settings.account_number,
        ),
        TrackingNumber=None,
        OriginDetail=PickupOriginDetail(
            UseAccountAddress=None,
            PickupLocation=ContactAndAddress(
                Contact=Contact(
                    ContactId=None,
                    PersonName=payload.address.person_name,
                    CompanyName=payload.address.company_name,
                    PhoneNumber=payload.address.phone_number,
                    EMailAddress=payload.address.email,
                ),
                Address=Address(
                    StreetLines=SF.concat_str(
                        payload.address.address_line1, payload.address.address_line2
                    ),
                    City=payload.address.city,
                    StateOrProvinceCode=payload.address.state_code,
                    PostalCode=payload.address.postal_code,
                    CountryCode=payload.address.country_code,
                    Residential=payload.address.residential,
                ),
            ),
            PackageLocation=payload.package_location,
            ReadyTimestamp=f"{payload.pickup_date}T{payload.ready_time}:00",
            CompanyCloseTime=f"{payload.closing_time}:00",
            PickupDateType=(
                PickupRequestType.SAME_DAY if same_day else PickupRequestType.FUTURE_DAY
            ).value,
            LastAccessTime=None,
            GeographicalPostalCode=None,
            Location=payload.package_location,
            DeleteLastUsed=None,
            SuppliesRequested=None,
            EarlyPickup=None,
        ),
        PickupServiceCategory=None,
        FreightPickupDetail=None,
        ExpressFreightDetail=None,
        PackageCount=len(packages) or 1,
        TotalWeight=Weight(Units=WeightUnits.LB.name, Value=packages.weight.LB)
        if len(packages) > 0
        else None,
        CarrierCode=CarrierCodeType.FDXE.value,
        OversizePackageCount=None,
        Remarks=payload.instruction,
        CommodityDescription=None,
        CountryRelationship=None,
    )

    return Serializable(request, _request_serializer)


def _request_serializer(request: CreatePickupRequest) -> str:
    envelope: Envelope = create_envelope(body_content=request)
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "v17")

    return XP.export(
        envelope,
        namespacedef_='xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v17="http://fedex.com/ws/pickup/v17"',
    )


def _get_availability(payload: PickupRequest, settings: Settings):
    data = pickup_availability_request(payload, settings)

    return Job(id="availability", data=data)


def _create_pickup(
    availability_response: str, payload: PickupRequest, settings: Settings
):
    availability = XP.build(PickupAvailabilityReply, XP.to_xml(availability_response))
    data = _pickup_request(payload, settings) if availability else None

    return Job(id="create_pickup", data=data, fallback="")
