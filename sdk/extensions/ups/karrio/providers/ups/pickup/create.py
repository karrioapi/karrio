from typing import Tuple, List
from functools import partial
from ups_lib.pickup_web_service_schema import (
    PickupCreationRequest,
    PickupCreationResponse,
    RequestType,
    ShipperType,
    PickupAddressType,
    WeightType,
    PickupDateInfoType,
    PhoneType,
    RateResultType,
    AccountType,
)
from karrio.core.units import Packages
from karrio.core.utils import (
    Serializable,
    create_envelope,
    Element,
    Job,
    Pipeline,
    NF,
    XP,
    DF,
    SF,
)
import karrio.lib as lib
from karrio.core.models import (
    PickupRequest,
    PickupDetails,
    Message,
    ChargeDetails,
)
from karrio.providers.ups.pickup.rate import pickup_rate_request
from karrio.providers.ups.error import parse_error_response
from karrio.providers.ups.units import PackagePresets, WeightUnit
from karrio.providers.ups.utils import Settings, default_request_serializer


def parse_pickup_response(
    _response: lib.Deserializable[Element], settings: Settings
) -> Tuple[PickupDetails, List[Message]]:
    response = _response.deserialize()
    reply = XP.find(
        "PickupCreationResponse", response, PickupCreationResponse, first=True
    )

    pickup = (
        _extract_pickup_details(response, settings)
        if reply is not None and reply.PRN is not None
        else None
    )

    return pickup, parse_error_response(response, settings)


def _extract_pickup_details(response: Element, settings: Settings) -> PickupDetails:
    pickup = XP.find(
        "PickupCreationResponse", response, PickupCreationResponse, first=True
    )
    rate = XP.find("RateResult", response, RateResultType, first=True)

    return PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=pickup.PRN,
        pickup_charge=ChargeDetails(
            name=rate.RateType,
            currency=rate.CurrencyCode,
            amount=NF.decimal(rate.GrandTotalOfAllCharge),
        ),
    )


def pickup_request(payload: PickupRequest, settings: Settings) -> Serializable:
    """
    Create a pickup request
    Steps
        1 - rate pickup
        2 - create pickup
    :param payload: PickupRequest
    :param settings: Settings
    :return: Serializable
    """
    request: Pipeline = Pipeline(
        rate=lambda *_: _rate_pickup(payload=payload, settings=settings),
        create=partial(_create_pickup, payload=payload, settings=settings),
    )
    return Serializable(request)


def _create_pickup_request(payload: PickupRequest, settings: Settings) -> Serializable:
    address = lib.to_address(payload.address)
    packages = Packages(payload.parcels, PackagePresets)
    has_overweight = any(package for package in packages if package.weight.KG > 32)

    request = create_envelope(
        header_content=settings.Security,
        body_content=PickupCreationRequest(
            Request=RequestType(),
            RatePickupIndicator="N",
            TaxInformationIndicator=None,
            UserLevelDiscountIndicator=None,
            Shipper=ShipperType(
                Account=AccountType(
                    AccountNumber=settings.account_number,
                    AccountCountryCode=address.country_code or "",
                ),
                ChargeCard=None,
                TaxInformation=None,
            ),
            PickupDateInfo=PickupDateInfoType(
                CloseTime=DF.ftime(payload.closing_time, "%H:%M", "%H%M"),
                ReadyTime=DF.ftime(payload.ready_time, "%H:%M", "%H%M"),
                PickupDate=DF.date(payload.pickup_date).strftime("%Y%m%d"),
            ),
            PickupAddress=PickupAddressType(
                CompanyName=address.company_name,
                ContactName=address.person_name,
                AddressLine=lib.join(
                    address.street,
                    address.address_line2,
                ),
                Room=None,
                Floor=None,
                City=address.city,
                StateProvince=address.state_code,
                Urbanization=None,
                PostalCode=address.postal_code,
                CountryCode=address.country_code,
                ResidentialIndicator=("Y" if address.residential else "N"),
                PickupPoint=payload.package_location,
                Phone=PhoneType(Number=address.phone_number or "000-000-0000"),
            ),
            AlternateAddressIndicator="Y",
            PickupPiece=None,
            TotalWeight=WeightType(
                Weight=packages.weight.LB, UnitOfMeasurement=WeightUnit.LB.value
            ),
            OverweightIndicator=("Y" if has_overweight else "N"),
            TrackingData=None,
            TrackingDataWithReferenceNumber=None,
            PaymentMethod="01",
            SpecialInstruction=payload.instruction,
            ReferenceNumber=None,
            FreightOptions=None,
            ServiceCategory=None,
            CashType=None,
            ShippingLabelsAvailable="Y",
        ),
    )

    return Serializable(
        request,
        default_request_serializer(
            "v11", 'xmlns:v11="http://www.ups.com/XMLSchema/XOLTWS/Pickup/v1.1"'
        ),
    )


def _rate_pickup(payload: PickupRequest, settings: Settings):
    data = pickup_rate_request(payload, settings)

    return Job(id="availability", data=data)


def _create_pickup(rate_response: str, payload: PickupRequest, settings: Settings):
    rate_result = XP.to_object(RateResultType, XP.to_xml(rate_response))
    data = _create_pickup_request(payload, settings) if rate_result else None

    return Job(id="create_pickup", data=data, fallback="")
