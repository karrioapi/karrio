from typing import List, Tuple, cast
from pyeshipper.quote_request import (
    EShipper, QuoteRequestType, FromType, ToType, PackagesType, PackageType
)
from pyeshipper.quote_reply import QuoteType, SurchargeType
from purplship.core.errors import FieldError, FieldErrorCode
from purplship.core.utils import Element, Serializable, concat_str, decimal
from purplship.core.models import RateRequest, RateDetails, Message, ChargeDetails
from purplship.core.units import Package, Options
from purplship.carriers.eshipper.utils import Settings, standard_request_serializer
from purplship.carriers.eshipper.units import Service, PackagingType, FreightClass, Option
from purplship.carriers.eshipper.error import parse_error_response


def parse_quote_reply(response: Element, settings: Settings) -> Tuple[List[RateDetails], List[Message]]:
    estimates = response.xpath(".//*[local-name() = $name]", name="Quote")
    return (
        [_extract_rate(node, settings) for node in estimates],
        parse_error_response(response, settings)
    )


def _extract_rate(node: Element, settings: Settings) -> RateDetails:
    quote = QuoteType()
    quote.build(node)
    service = next(
        (s.name for s in Service if str(quote.serviceId) == s.value),
        quote.serviceId
    )
    surcharges = [ChargeDetails(
        name=charge.name,
        amount=decimal(charge.amount),
        currency=quote.currency
    ) for charge in cast(List[SurchargeType], quote.Surcharge)]

    fuel_surcharge = ChargeDetails(
        name="Fuel surcharge",
        amount=decimal(quote.fuelSurcharge),
        currency=quote.currency
    ) if quote.fuelSurcharge is not None else None

    return RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        currency=quote.currency,
        service=service,
        base_charge=decimal(quote.baseCharge),
        total_charge=decimal(quote.totalCharge),
        transit_days=quote.transitDays,
        extra_charges=[fuel_surcharge] + surcharges
    )


def quote_request(payload: RateRequest, settings: Settings) -> Serializable[EShipper]:
    package = Package(payload.parcel)

    dimensions = [
        ("parcel.weight", package.weight.value), ("parcel.height", package.height.value),
        ("parcel.width", package.width.value), ("parcel.length", package.length.value)
    ]
    field_errors = {key: FieldErrorCode.required for key, dim in dimensions if dim is None}
    if any(field_errors.items()):
        raise FieldError(field_errors)

    packaging_type = PackagingType[package.packaging_type or "small_box"].value
    packaging = "Pallet" if packaging_type in [PackagingType.pallet.value] else "Package"
    options = Options(payload.options)
    service = next(
        (Service[s].value for s in payload.services if s in Service.__members__),
        "0"
    )
    freight_class = next(
        (FreightClass[c].value for c in payload.options.keys() if c in FreightClass.__members__),
        None
    )
    special_services = {
        Option[s]: "true" for s in payload.options.keys() if s in Option.__members__
    }

    request = EShipper(
        username=settings.username,
        password=settings.password,
        version="3.0.0",
        QuoteRequest=QuoteRequestType(
            saturdayPickupRequired=special_services.get(Option.eshipper_saturday_pickup_required),
            homelandSecurity=special_services.get(Option.eshipper_homeland_security),
            pierCharge=None,
            exhibitionConventionSite=special_services.get(Option.eshipper_exhibition_convention_site),
            militaryBaseDelivery=special_services.get(Option.eshipper_military_base_delivery),
            customsIn_bondFreight=special_services.get(Option.eshipper_customs_in_bond_freight),
            limitedAccess=special_services.get(Option.eshipper_limited_access),
            excessLength=special_services.get(Option.eshipper_excess_length),
            tailgatePickup=special_services.get(Option.eshipper_tailgate_pickup),
            residentialPickup=special_services.get(Option.eshipper_residential_pickup),
            crossBorderFee=None,
            notifyRecipient=special_services.get(Option.eshipper_notify_recipient),
            singleShipment=special_services.get(Option.eshipper_single_shipment),
            tailgateDelivery=special_services.get(Option.eshipper_tailgate_delivery),
            residentialDelivery=special_services.get(Option.eshipper_residential_delivery),
            insuranceType=options.insurance is not None,
            scheduledShipDate=None,
            insideDelivery=special_services.get(Option.eshipper_inside_delivery),
            isSaturdayService=special_services.get(Option.eshipper_is_saturday_service),
            dangerousGoodsType=special_services.get(Option.eshipper_dangerous_goods_type),
            serviceId=service,
            stackable=special_services.get(Option.eshipper_stackable),
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
                country=payload.shipper.country_code
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
                country=payload.recipient.country_code
            ),
            COD=None,
            Packages=PackagesType(
                Package=[
                    PackageType(
                        length=package.length.value,
                        width=package.width.value,
                        height=package.height.value,
                        weight=package.weight.value,
                        type_=packaging_type,
                        freightClass=freight_class,
                        nmfcCode=None,
                        insuranceAmount=None,
                        codAmount=None,
                        description=payload.parcel.description,
                    )
                ],
                type_=packaging
            ),
        )
    )

    return Serializable(request, standard_request_serializer)
