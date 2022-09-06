from eshipper_lib.quote_reply import QuoteType
from eshipper_lib.quote_request import (
    EShipper,
    QuoteRequestType,
    FromType,
    ToType,
    PackagesType,
    PackageType,
)

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.eshipper.error as provider_error
import karrio.providers.eshipper.units as provider_units
import karrio.providers.eshipper.utils as provider_utils


def parse_quote_reply(
    response: lib.Element, settings: provider_utils.Settings
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    estimates = lib.find_element("Quote", response)
    return (
        [_extract_rate(node, settings) for node in estimates],
        provider_error.parse_error_response(response, settings),
    )


def _extract_rate(
    node: lib.Element, settings: provider_utils.Settings
) -> models.RateDetails:
    quote = lib.to_object(QuoteType, node)
    rate_provider, service, service_name = provider_units.ShippingService.info(
        quote.serviceId, quote.carrierId, quote.serviceName, quote.carrierName
    )
    charges = [
        ("Base charge", quote.baseCharge),
        ("Fuel surcharge", quote.fuelSurcharge),
        *((surcharge.name, surcharge.amount) for surcharge in quote.Surcharge),
    ]

    return models.RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        currency=quote.currency,
        service=service,
        total_charge=lib.to_decimal(quote.totalCharge),
        transit_days=quote.transitDays,
        extra_charges=[
            models.ChargeDetails(
                name=name,
                currency="CAD",
                amount=lib.to_decimal(amount),
            )
            for name, amount in charges
            if amount
        ],
        meta=dict(rate_provider=rate_provider, service_name=service_name),
    )


def quote_request(
    payload: models.RateRequest, settings: provider_utils.Settings
) -> lib.Serializable[EShipper]:
    packages = lib.to_packages(
        payload.parcels,
        package_option_type=provider_units.ShippingOption,
        required=["weight", "height", "width", "length"],
    )
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    packaging_type = provider_units.PackagingType[
        packages.package_type or "eshipper_boxes"
    ].value
    packaging = (
        "Pallet"
        if packaging_type in [provider_units.PackagingType.pallet.value]
        else "Package"
    )
    service = (
        lib.to_services(payload.services, provider_units.ShippingService).first
        or provider_units.ShippingService.eshipper_all
    )

    request = EShipper(
        username=settings.username,
        password=settings.password,
        version="3.0.0",
        QuoteRequest=QuoteRequestType(
            saturdayPickupRequired=options.eshipper_saturday_pickup_required.state,
            homelandSecurity=options.eshipper_homeland_security.state,
            pierCharge=None,
            exhibitionConventionSite=options.eshipper_exhibition_convention_site.state,
            militaryBaseDelivery=options.eshipper_military_base_delivery.state,
            customsIn_bondFreight=options.eshipper_customs_in_bond_freight.state,
            limitedAccess=options.eshipper_limited_access.state,
            excessLength=options.eshipper_excess_length.state,
            tailgatePickup=options.eshipper_tailgate_pickup.state,
            residentialPickup=options.eshipper_residential_pickup.state,
            crossBorderFee=None,
            notifyRecipient=options.eshipper_notify_recipient.state,
            singleShipment=options.eshipper_single_shipment.state,
            tailgateDelivery=options.eshipper_tailgate_delivery.state,
            residentialDelivery=options.eshipper_residential_delivery.state,
            insuranceType=options.insurance.state is not None,
            scheduledShipDate=None,
            insideDelivery=options.eshipper_inside_delivery.state,
            isSaturdayService=options.eshipper_is_saturday_service.state,
            dangerousGoodsType=options.eshipper_dangerous_goods_type.state,
            serviceId=service.value,
            stackable=options.eshipper_stackable.state,
            From=FromType(
                id=None,
                company=payload.shipper.company_name or " ",
                instructions=None,
                email=payload.shipper.email,
                attention=payload.shipper.person_name,
                phone=payload.shipper.phone_number,
                tailgateRequired=None,
                residential=payload.shipper.residential,
                address1=lib.join(payload.shipper.address_line1, join=True),
                address2=lib.join(payload.shipper.address_line2, join=True),
                city=payload.shipper.city,
                state=payload.shipper.state_code,
                zip=payload.shipper.postal_code,
                country=payload.shipper.country_code,
            ),
            To=ToType(
                id=None,
                company=payload.recipient.company_name or " ",
                notifyRecipient=None,
                instructions=None,
                email=payload.recipient.email,
                attention=payload.recipient.person_name,
                phone=payload.recipient.phone_number,
                tailgateRequired=None,
                residential=payload.recipient.residential,
                address1=lib.join(payload.recipient.address_line1, join=True),
                address2=lib.join(payload.recipient.address_line2, join=True),
                city=payload.recipient.city,
                state=payload.recipient.state_code,
                zip=payload.recipient.postal_code,
                country=payload.recipient.country_code,
            ),
            COD=None,
            Packages=PackagesType(
                Package=[
                    PackageType(
                        length=provider_utils.ceil(package.length.IN),
                        width=provider_utils.ceil(package.width.IN),
                        height=provider_utils.ceil(package.height.IN),
                        weight=provider_utils.ceil(package.weight.LB),
                        type_=packaging_type,
                        freightClass=package.parcel.freight_class,
                        nmfcCode=None,
                        insuranceAmount=package.options.insurance.state,
                        codAmount=package.options.cash_on_delivery.state,
                        description=package.parcel.description,
                    )
                    for package in packages
                ],
                type_=packaging,
            ),
        ),
    )

    return lib.Serializable(request, provider_utils.standard_request_serializer)
