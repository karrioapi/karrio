from typing import List, Tuple, cast
from eshipper_lib.quote_request import (
    EShipper,
    QuoteRequestType,
    FromType,
    ToType,
    PackagesType,
    PackageType,
)
from eshipper_lib.quote_reply import QuoteType, SurchargeType
from karrio.core.utils import Element, Serializable, SF, NF, XP
from karrio.core.models import RateRequest, RateDetails, Message, ChargeDetails
from karrio.core.units import Packages, Options, Services
from karrio.providers.eshipper.utils import (
    Settings,
    standard_request_serializer,
    ceil,
)
from karrio.providers.eshipper.units import (
    Service,
    PackagingType,
    FreightClass,
    Option,
)
from karrio.providers.eshipper.error import parse_error_response


def parse_quote_reply(
    response: Element, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    estimates = XP.find("Quote", response)
    return (
        [_extract_rate(node, settings) for node in estimates],
        parse_error_response(response, settings),
    )


def _extract_rate(node: Element, settings: Settings) -> RateDetails:
    quote = XP.build(QuoteType, node)
    rate_provider, service, service_name = Service.info(
        quote.serviceId, quote.carrierId, quote.serviceName, quote.carrierName
    )
    surcharges = [
        ChargeDetails(
            name=charge.name,
            amount=NF.decimal(charge.amount),
            currency=quote.currency
        )
        for charge in cast(List[SurchargeType], quote.Surcharge)
    ]
    fuel_surcharge = (
        ChargeDetails(
            name="Fuel surcharge",
            amount=NF.decimal(quote.fuelSurcharge),
            currency=quote.currency,
        )
        if quote.fuelSurcharge is not None else None
    )

    return RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        currency=quote.currency,
        service=service,
        base_charge=NF.decimal(quote.baseCharge),
        total_charge=NF.decimal(quote.totalCharge),
        transit_days=quote.transitDays,
        extra_charges=([fuel_surcharge] + surcharges),
        meta=dict(
            rate_provider=rate_provider,
            service_name=service_name
        )
    )


def quote_request(payload: RateRequest, settings: Settings) -> Serializable[EShipper]:
    options = Options(payload.options, Option)
    packages = Packages(payload.parcels, required=["weight", "height", "width", "length"])
    packaging_type = PackagingType[packages.package_type or "eshipper_boxes"].value
    packaging = ("Pallet" if packaging_type in [PackagingType.pallet.value] else "Package")
    service = (Services(payload.services, Service).first or Service.eshipper_all)

    freight_class = next(
        (FreightClass[c].value for c in payload.options.keys() if c in FreightClass),
        None,
    )

    request = EShipper(
        username=settings.username,
        password=settings.password,
        version="3.0.0",
        QuoteRequest=QuoteRequestType(
            saturdayPickupRequired=options.eshipper_saturday_pickup_required,
            homelandSecurity=options.eshipper_homeland_security,
            pierCharge=None,
            exhibitionConventionSite=options.eshipper_exhibition_convention_site,
            militaryBaseDelivery=options.eshipper_military_base_delivery,
            customsIn_bondFreight=options.eshipper_customs_in_bond_freight,
            limitedAccess=options.eshipper_limited_access,
            excessLength=options.eshipper_excess_length,
            tailgatePickup=options.eshipper_tailgate_pickup,
            residentialPickup=options.eshipper_residential_pickup,
            crossBorderFee=None,
            notifyRecipient=options.eshipper_notify_recipient,
            singleShipment=options.eshipper_single_shipment,
            tailgateDelivery=options.eshipper_tailgate_delivery,
            residentialDelivery=options.eshipper_residential_delivery,
            insuranceType=options.insurance is not None,
            scheduledShipDate=None,
            insideDelivery=options.eshipper_inside_delivery,
            isSaturdayService=options.eshipper_is_saturday_service,
            dangerousGoodsType=options.eshipper_dangerous_goods_type,
            serviceId=service.value,
            stackable=options.eshipper_stackable,
            From=FromType(
                id=payload.shipper.id,
                company=payload.shipper.company_name or " ",
                instructions=None,
                email=payload.shipper.email,
                attention=payload.shipper.person_name,
                phone=payload.shipper.phone_number,
                tailgateRequired=None,
                residential=payload.shipper.residential,
                address1=SF.concat_str(payload.shipper.address_line1, join=True),
                address2=SF.concat_str(payload.shipper.address_line2, join=True),
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
                address1=SF.concat_str(payload.recipient.address_line1, join=True),
                address2=SF.concat_str(payload.recipient.address_line2, join=True),
                city=payload.recipient.city,
                state=payload.recipient.state_code,
                zip=payload.recipient.postal_code,
                country=payload.recipient.country_code,
            ),
            COD=None,
            Packages=PackagesType(
                Package=[
                    PackageType(
                        length=ceil(package.length.IN),
                        width=ceil(package.width.IN),
                        height=ceil(package.height.IN),
                        weight=ceil(package.weight.LB),
                        type_=packaging_type,
                        freightClass=freight_class,
                        nmfcCode=None,
                        insuranceAmount=None,
                        codAmount=None,
                        description=package.parcel.description,
                    )
                    for package in packages
                ],
                type_=packaging,
            ),
        ),
    )

    return Serializable(request, standard_request_serializer)
