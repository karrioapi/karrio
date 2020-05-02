from typing import List, Tuple
from pyfedex.pickup_service_v20 import (
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
    CarrierCodeType
)
from purplship.core.models import PickupRequest, PickupDetails, Message
from purplship.core.units import Package
from purplship.core.utils import (
    Serializable, export, create_envelope, apply_namespaceprefix, Envelope, concat_str, Element
)
from purplship.providers.fedex.utils import Settings
from purplship.providers.fedex.error import parse_error_response


def parse_pickup_response(response: Element, settings: Settings) -> Tuple[PickupDetails, List[Message]]:
    pickup = (
        _extract_pickup_details(response, settings)
    )
    return pickup, parse_error_response(response, settings)


def _extract_pickup_details(response: Element, settings: Settings) -> PickupDetails:

    return PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number="",
    )


def pickup_request(payload: PickupRequest, settings: Settings) -> Serializable[CreatePickupRequest]:
    packages: List[Package] = [Package(parcel) for parcel in payload.parcels]

    request = CreatePickupRequest(
        WebAuthenticationDetail=settings.webAuthenticationDetail,
        ClientDetail=settings.clientDetail,
        TransactionDetail=TransactionDetail(CustomerTransactionId="FTC"),
        Version=VersionId(ServiceId="disp", Major=17, Intermediate=0, Minor=0),
        AssociatedAccountNumber=AssociatedAccount(
            Type=AssociatedAccountNumberType.FEDEX_EXPRESS,
            AccountNumber=settings.account_number
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
                    EMailAddress=payload.address.email
                ),
                Address=Address(
                    StreetLines=concat_str(payload.address.address_line1, payload.address.address_line2),
                    City=payload.address.city,
                    StateOrProvinceCode=payload.address.state_code,
                    PostalCode=payload.address.postal_code,
                    CountryCode=payload.address.country_code,
                    Residential=payload.address.residential,
                )
            ),
            PackageLocation=payload.package_location,
            ReadyTimestamp=f'{payload.ready_time}:00',
            CompanyCloseTime=f'{payload.closing_time}:00',
            PickupDateType=None,
            LastAccessTime=None,
            GeographicalPostalCode=None,
            Location=None,
            DeleteLastUsed=None,
            SuppliesRequested=None,
            EarlyPickup=None
        ),
        PickupServiceCategory=None,
        FreightPickupDetail=None,
        ExpressFreightDetail=None,
        PackageCount=len(packages),
        TotalWeight=Weight(
            Units=WeightUnits.LB.name,
            Value=sum((p.weight.LB or 0.0) for p in packages)
        ),
        CarrierCode=CarrierCodeType.FDXE.name,
        OversizePackageCount=None,
        Remarks=payload.instruction,
        CommodityDescription=None,
        CountryRelationship=None
    )

    return Serializable(request, _request_serializer)


def _request_serializer(request: CreatePickupRequest) -> str:
    envelope: Envelope = create_envelope(body_content=request)
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "v17")

    return export(
        envelope,
        namespacedef_='xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v17="http://fedex.com/ws/pickup/v17"'
    )
