from typing import List, Tuple, cast
from pyfreightcom.quote_request import (
    Freightcom,
    QuoteRequestType,
    FromType,
    ToType,
    PackagesType,
    PackageType,
)
from pyfreightcom.quote_reply import QuoteType, SurchargeType
from purplship.core.utils import Element, Serializable, concat_str, decimal
from purplship.core.models import RateRequest, RateDetails, Message, ChargeDetails
from purplship.core.units import Packages, Options
from purplship.providers.freightcom.utils import (
    Settings,
    standard_request_serializer,
    ceil,
)
from purplship.providers.freightcom.units import (
    Service,
    FreightPackagingType,
    FreightClass,
    Option,
)
from purplship.providers.freightcom.error import parse_error_response


def parse_quote_reply(
    response: Element, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    estimates = response.xpath(".//*[local-name() = $name]", name="Quote")
    return (
        [_extract_rate(node, settings) for node in estimates],
        parse_error_response(response, settings),
    )


def _extract_rate(node: Element, settings: Settings) -> RateDetails:
    quote = QuoteType()
    quote.build(node)
    service = next(
        (s.name for s in Service if str(quote.serviceId) == s.value), quote.serviceId
    )
    surcharges = [
        ChargeDetails(
            name=charge.name, amount=decimal(charge.amount), currency=quote.currency
        )
        for charge in cast(List[SurchargeType], quote.Surcharge)
    ]

    fuel_surcharge = (
        ChargeDetails(
            name="Fuel surcharge",
            amount=decimal(quote.fuelSurcharge),
            currency=quote.currency,
        )
        if quote.fuelSurcharge is not None
        else None
    )

    return RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        currency=quote.currency,
        service=service,
        base_charge=decimal(quote.baseCharge),
        total_charge=decimal(quote.totalCharge),
        transit_days=quote.transitDays,
        extra_charges=[fuel_surcharge] + surcharges,
    )


def quote_request(payload: RateRequest, settings: Settings) -> Serializable[Freightcom]:
    packages = Packages(payload.parcels, required=["weight", "height", "width", "length"])
    packaging_type = (
        FreightPackagingType[packages[0].packaging_type or "small_box"].value
        if len(packages) == 1 else "small_box"
    )

    options = Options(payload.options)
    service = next(
        (Service[s].value for s in payload.services if s in Service.__members__), None
    )
    freight_class = next(
        (
            FreightClass[c].value
            for c in payload.options.keys()
            if c in FreightClass.__members__
        ),
        None,
    )
    special_services = {
        Option[s]: True for s in payload.options.keys() if s in Option.__members__
    }

    request = Freightcom(
        username=settings.username,
        password=settings.password,
        version="3.1.0",
        QuoteRequest=QuoteRequestType(
            saturdayPickupRequired=special_services.get(
                Option.freightcom_saturday_pickup_required
            ),
            homelandSecurity=special_services.get(Option.freightcom_homeland_security),
            pierCharge=None,
            exhibitionConventionSite=special_services.get(
                Option.freightcom_exhibition_convention_site
            ),
            militaryBaseDelivery=special_services.get(
                Option.freightcom_military_base_delivery
            ),
            customsIn_bondFreight=special_services.get(
                Option.freightcom_customs_in_bond_freight
            ),
            limitedAccess=special_services.get(Option.freightcom_limited_access),
            excessLength=special_services.get(Option.freightcom_excess_length),
            tailgatePickup=special_services.get(Option.freightcom_tailgate_pickup),
            residentialPickup=special_services.get(
                Option.freightcom_residential_pickup
            ),
            crossBorderFee=None,
            notifyRecipient=special_services.get(Option.freightcom_notify_recipient),
            singleShipment=special_services.get(Option.freightcom_single_shipment),
            tailgateDelivery=special_services.get(Option.freightcom_tailgate_delivery),
            residentialDelivery=special_services.get(
                Option.freightcom_residential_delivery
            ),
            insuranceType=options.insurance is not None,
            scheduledShipDate=None,
            insideDelivery=special_services.get(Option.freightcom_inside_delivery),
            isSaturdayService=special_services.get(
                Option.freightcom_is_saturday_service
            ),
            dangerousGoodsType=special_services.get(
                Option.freightcom_dangerous_goods_type
            ),
            serviceId=service,
            stackable=special_services.get(Option.freightcom_stackable),
            From=FromType(
                id=payload.shipper.id,
                company=payload.shipper.company_name or " ",
                instructions=None,
                email=payload.shipper.email,
                attention=payload.shipper.person_name,
                phone=payload.shipper.phone_number,
                tailgateRequired=None,
                residential=payload.shipper.residential,
                address1=concat_str(payload.shipper.address_line1, join=True),
                address2=concat_str(payload.shipper.address_line2, join=True),
                city=payload.shipper.city,
                state=payload.shipper.state_code,
                zip=payload.shipper.postal_code,
                country=payload.shipper.country_code,
            ),
            To=ToType(
                id=payload.recipient.id,
                company=payload.recipient.company_name or " ",
                notifyRecipient=None,
                instructions=None,
                email=payload.recipient.email,
                attention=payload.recipient.person_name,
                phone=payload.recipient.phone_number,
                tailgateRequired=None,
                residential=payload.recipient.residential,
                address1=concat_str(payload.recipient.address_line1, join=True),
                address2=concat_str(payload.recipient.address_line2, join=True),
                city=payload.recipient.city,
                state=payload.recipient.state_code,
                zip=payload.recipient.postal_code,
                country=payload.recipient.country_code,
            ),
            COD=None,
            Packages=PackagesType(
                Package=[
                    PackageType(
                        length=ceil(package.length.value),
                        width=ceil(package.width.value),
                        height=ceil(package.height.value),
                        weight=ceil(package.weight.value),
                        type_=packaging_type,
                        freightClass=freight_class,
                        nmfcCode=None,
                        insuranceAmount=None,
                        codAmount=None,
                        description=package.parcel.description,
                    )
                    for package in packages
                ],
                type_="Package",
            ),
        ),
    )

    return Serializable(request, standard_request_serializer)
