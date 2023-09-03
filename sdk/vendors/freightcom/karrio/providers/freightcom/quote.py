from karrio.schemas.freightcom.quote_request import (
    Freightcom,
    QuoteRequestType,
    FromType,
    ToType,
    PackagesType,
    PackageType,
)
from karrio.schemas.freightcom.quote_reply import QuoteType

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.freightcom.error as provider_error
import karrio.providers.freightcom.units as provider_units
import karrio.providers.freightcom.utils as provider_utils


def parse_quote_reply(
    _response: lib.Deserializable[lib.Element], settings: provider_utils.Settings
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    estimates = lib.find_element("Quote", response)

    return (
        [_extract_rate(node, settings) for node in estimates],
        provider_error.parse_error_response(response, settings),
    )


def _extract_rate(
    node: lib.Element,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    quote = lib.to_object(QuoteType, node)
    rate_provider, service, service_name = provider_units.ShippingService.info(
        quote.serviceId,
        quote.carrierId,
        quote.serviceName,
        quote.carrierName,
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
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
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
    packaging_type = provider_units.FreightPackagingType[
        packages.package_type or "small_box"
    ].value
    packaging = (
        "Pallet"
        if packaging_type in [provider_units.FreightPackagingType.pallet.value]
        else "Package"
    )
    service = (
        lib.to_services(payload.services, provider_units.ShippingService).first
        or provider_units.ShippingService.freightcom_all
    )

    request = Freightcom(
        username=settings.username,
        password=settings.password,
        version="3.1.0",
        QuoteRequest=QuoteRequestType(
            saturdayPickupRequired=options.freightcom_saturday_pickup_required.state,
            homelandSecurity=options.freightcom_homeland_security.state,
            pierCharge=None,
            exhibitionConventionSite=options.freightcom_exhibition_convention_site.state,
            militaryBaseDelivery=options.freightcom_military_base_delivery.state,
            customsIn_bondFreight=options.freightcom_customs_in_bond_freight.state,
            limitedAccess=options.freightcom_limited_access.state,
            excessLength=options.freightcom_excess_length.state,
            tailgatePickup=options.freightcom_tailgate_pickup.state,
            residentialPickup=options.freightcom_residential_pickup.state,
            crossBorderFee=None,
            notifyRecipient=options.freightcom_notify_recipient.state,
            singleShipment=options.freightcom_single_shipment.state,
            tailgateDelivery=options.freightcom_tailgate_delivery.state,
            residentialDelivery=options.freightcom_residential_delivery.state,
            insuranceType=options.insurance.state is not None,
            scheduledShipDate=None,
            insideDelivery=options.freightcom_inside_delivery.state,
            isSaturdayService=options.freightcom_is_saturday_service.state,
            dangerousGoodsType=options.freightcom_dangerous_goods_type.state,
            serviceId=service.value,
            stackable=options.freightcom_stackable.state,
            From=FromType(
                id=None,
                company=shipper.company_name or " ",
                instructions=None,
                email=shipper.email,
                attention=shipper.person_name,
                phone=shipper.phone_number,
                tailgateRequired=None,
                residential=shipper.residential,
                address1=shipper.street,
                address2=lib.text(shipper.address_line2),
                city=shipper.city,
                state=shipper.state_code,
                zip=shipper.postal_code,
                country=shipper.country_code,
            ),
            To=ToType(
                id=None,
                company=recipient.company_name or " ",
                notifyRecipient=None,
                instructions=None,
                email=recipient.email,
                attention=recipient.person_name,
                phone=recipient.phone_number,
                tailgateRequired=None,
                residential=recipient.residential,
                address1=recipient.street,
                address2=lib.text(recipient.address_line2),
                city=recipient.city,
                state=recipient.state_code,
                zip=recipient.postal_code,
                country=recipient.country_code,
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
