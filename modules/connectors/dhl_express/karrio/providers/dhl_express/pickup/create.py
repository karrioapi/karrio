from typing import Tuple, List
import karrio.schemas.dhl_express.book_pickup_global_req_3_0 as dhl
from karrio.schemas.dhl_express.book_pickup_global_res_3_0 import BookPUResponse
from karrio.schemas.dhl_express.pickupdatatypes_global_3_0 import (
    Requestor,
    Pickup,
    WeightSeg,
    RequestorContact,
)
import karrio.schemas.dhl_express.datatypes_global_v62 as dhl_global
import karrio.lib as lib
from karrio.core.utils import (
    Serializable,
    Element,
    DF,
    NF,
    XP,
)
from karrio.core.models import (
    PickupRequest,
    Message,
    PickupDetails,
    ChargeDetails,
)
from karrio.core.units import WeightUnit, Weight, Packages
from karrio.providers.dhl_express.units import (
    CountryRegion,
    WeightUnit as DHLWeightUnit,
)
from karrio.providers.dhl_express.utils import Settings, reformat_time
from karrio.providers.dhl_express.error import parse_error_response


def parse_pickup_response(
    _response: lib.Deserializable[lib.Element],
    settings: Settings,
) -> Tuple[PickupDetails, List[Message]]:
    response = _response.deserialize()
    successful = len(lib.find_element("ConfirmationNumber", response)) > 0
    pickup = _extract_pickup(response, settings) if successful else None
    return pickup, parse_error_response(response, settings)


def _extract_pickup(response: Element, settings: Settings) -> PickupDetails:
    pickup = BookPUResponse()
    pickup.build(response)
    pickup_charge = (
        ChargeDetails(
            name="Pickup Charge",
            amount=NF.decimal(pickup.PickupCharge),
            currency=pickup.CurrencyCode,
        )
        if pickup.PickupCharge is not None
        else None
    )
    return PickupDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        confirmation_number=str(pickup.ConfirmationNumber[0]),
        pickup_date=DF.fdate(pickup.NextPickupDate),
        pickup_charge=pickup_charge,
        ready_time=DF.ftime(pickup.ReadyByTime),
        closing_time=DF.ftime(pickup.CallInTime),
    )


def pickup_request(payload: PickupRequest, settings: Settings) -> Serializable:
    packages = Packages(payload.parcels)
    address = lib.to_address(payload.address)

    request = dhl.BookPURequest(
        Request=settings.Request(
            MetaData=dhl.MetaData(SoftwareName="XMLPI", SoftwareVersion=3.0)
        ),
        schemaVersion=3.0,
        RegionCode=(
            CountryRegion[address.country_code].value if address.country_code else "AM"
        ),
        Requestor=Requestor(
            AccountNumber=settings.account_number,
            AccountType="D",
            RequestorContact=RequestorContact(
                PersonName=address.person_name,
                Phone=address.phone_number,
                PhoneExtension=None,
            ),
            CompanyName=address.company_name,
        ),
        Place=dhl.Place1(
            City=address.city,
            StateCode=address.state_code,
            PostalCode=address.postal_code,
            CompanyName=address.company_name,
            CountryCode=address.country_code,
            PackageLocation=payload.package_location,
            LocationType="R" if address.residential else "B",
            Address1=address.street,
            Address2=address.address_line2,
        ),
        PickupContact=RequestorContact(
            PersonName=address.contact,
            Phone=address.phone_number,
        ),
        Pickup=Pickup(
            Pieces=len(payload.parcels),
            PickupDate=payload.pickup_date,
            ReadyByTime=f"{payload.ready_time}:00",
            CloseTime=f"{payload.closing_time}:00",
            SpecialInstructions=[payload.instruction],
            RemotePickupFlag="Y",
            weight=WeightSeg(
                Weight=packages.weight.value,
                WeightUnit=DHLWeightUnit[packages.weight.unit].value,
            ),
        ),
        ShipmentDetails=None,
        ConsigneeDetails=None,
    )

    return Serializable(request, _request_serializer)


def _request_serializer(request: dhl.BookPURequest) -> str:
    xml_str = (
        XP.export(
            request,
            name_="req:BookPURequest",
            namespacedef_='xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com book-pickup-global-req_EA.xsd"',
        )
        .replace("dhlPickup:", "")
        .replace('schemaVersion="3"', 'schemaVersion="3.0"')
    )

    xml_str = reformat_time("CloseTime", reformat_time("ReadyByTime", xml_str))
    return xml_str
