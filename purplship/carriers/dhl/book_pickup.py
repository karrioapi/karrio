from typing import Tuple, List
from pydhl.book_pickup_global_req_3_0 import BookPURequest
from pydhl.book_pickup_global_res_3_0 import BookPUResponse
from pydhl.pickupdatatypes_global_3_0 import (
    Requestor, Place, Contact, Pickup, WeightSeg
)
from purplship.core.utils.helpers import export
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.xml import Element
from purplship.core.models import (
    PickupRequest, Error, PickupDetails, ChargeDetails, TimeDetails
)
from purplship.carriers.dhl.units import CountryRegion
from purplship.carriers.dhl.utils import Settings, reformat_time
from purplship.carriers.dhl.error import parse_error_response


def parse_book_pickup_response(response, settings: Settings) -> Tuple[PickupDetails, List[Error]]:
    successful = len(response.xpath(".//*[local-name() = $name]", name="ConfirmationNumber")) > 0
    pickup = _extract_pickup(response, settings) if successful else None
    return pickup, parse_error_response(response, settings)


def _extract_pickup(response: Element, settings: Settings) -> PickupDetails:
    pickup = BookPUResponse()
    pickup.build(response)
    pickup_charge = (
        ChargeDetails(name="Pickup Charge", amount=pickup.PickupCharge, currency=pickup.CurrencyCode)
        if pickup.PickupCharge is not None else None
    )
    ref_times = (
        [] if pickup.ReadyByTime is None else [TimeDetails(name="ReadyByTime", value=pickup.ReadyByTime)] +
        [] if pickup.CallInTime is None else [TimeDetails(name="CallInTime", value=pickup.CallInTime)]
    )
    return PickupDetails(
        carrier=settings.carrier_name,
        confirmation_number=pickup.ConfirmationNumber,
        pickup_date=pickup.NextPickupDate,
        pickup_charge=pickup_charge,
        ref_times=ref_times,
    )


def book_pickup_request(payload: PickupRequest, settings: Settings) -> Serializable[BookPURequest]:
    request = BookPURequest(
        Request=settings.Request(),
        schemaVersion="1.0",
        RegionCode=CountryRegion[payload.country_code].value if payload.country_code else "AM",
        Requestor=Requestor(
            AccountNumber=payload.account_number,
            AccountType="D",
            RequestorContact=None,
            CompanyName=None,
        ),
        Place=Place(
            City=payload.city,
            StateCode=payload.state_code,
            PostalCode=payload.postal_code,
            CompanyName=payload.company_name,
            CountryCode=payload.country_code,
            PackageLocation=payload.package_location or "...",
            LocationType="B" if payload.is_business else "R",
            Address1=(payload.address_lines[0] if len(payload.address_lines) > 0 else None),
            Address2=(payload.address_lines[1] if len(payload.address_lines) > 1 else None),
        ),
        PickupContact=Contact(PersonName=payload.person_name, Phone=payload.phone_number),
        Pickup=Pickup(
            Pieces=payload.pieces,
            PickupDate=payload.date,
            ReadyByTime=payload.ready_time,
            CloseTime=payload.closing_time,
            SpecialInstructions=payload.instruction,
            RemotePickupFlag=None,
            weight=(
                WeightSeg(Weight=payload.weight, WeightUnit=payload.weight_unit)
                if any([payload.weight, payload.weight_unit]) else None
            ),
        ),
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: BookPURequest) -> str:
    xml_str = (
        export(
            request,
            name_="req:BookPURequest",
            namespacedef_='xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com book-pickup-global-req.xsd"',
        )
        .replace("dhlPickup:", "")
        .replace('schemaVersion="1."', 'schemaVersion="1.0"')
    )

    xml_str = reformat_time("CloseTime", reformat_time("ReadyByTime", xml_str))
    return xml_str
