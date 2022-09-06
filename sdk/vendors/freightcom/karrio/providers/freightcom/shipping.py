from freightcom_lib.shipping_request import (
    Freightcom,
    ShippingRequestType,
    FromType,
    ToType,
    PackagesType,
    PackageType,
    PaymentType as RequestPaymentType,
    CODType,
    CODReturnAddressType,
    ContactType,
    ReferenceType,
    CustomsInvoiceType,
    ItemType,
    BillToType,
)
from freightcom_lib.shipping_reply import (
    ShippingReplyType,
    QuoteType,
)

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.freightcom.error as provider_error
import karrio.providers.freightcom.units as provider_units
import karrio.providers.freightcom.utils as provider_utils


def parse_shipping_reply(
    response: lib.Element, settings: provider_utils.Settings
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    shipping_node = lib.find_element("ShippingReply", response, first=True)
    shipment = (
        _extract_shipment(shipping_node, settings)
        if shipping_node is not None
        else None
    )

    return shipment, provider_error.parse_error_response(response, settings)


def _extract_shipment(
    node: lib.Element,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    shipping = lib.to_object(ShippingReplyType, node)
    quote: QuoteType = shipping.Quote or QuoteType()

    tracking_number = getattr(
        next(iter(shipping.Package), None), "trackingNumber", None
    )
    rate_provider, service, service_name = provider_units.ShippingService.info(
        quote.serviceId, quote.carrierId, quote.serviceName, quote.carrierName
    )
    charges = [
        ("Base charge", quote.baseCharge),
        ("Fuel surcharge", quote.fuelSurcharge),
        *((surcharge.name, surcharge.amount) for surcharge in quote.Surcharge),
    ]

    return models.ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=tracking_number,
        shipment_identifier=shipping.Order.id,
        selected_rate=(
            models.RateDetails(
                carrier_name=settings.carrier_name,
                carrier_id=settings.carrier_id,
                service=service,
                currency=quote.currency,
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
            if shipping.Quote is not None
            else None
        ),
        docs=models.Documents(label=shipping.Labels),
        meta=dict(
            rate_provider=rate_provider,
            service_name=service_name,
            tracking_url=shipping.TrackingURL,
        ),
    )


def shipping_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable[Freightcom]:
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

    service = provider_units.ShippingService.map(payload.service).value_or_key
    packaging_type = provider_units.FreightPackagingType[
        packages.package_type or "small_box"
    ].value
    packaging = (
        "Pallet"
        if packaging_type in [provider_units.FreightPackagingType.pallet.value]
        else "Package"
    )
    payment_type = (
        provider_units.PaymentType[payload.payment.paid_by] if payload.payment else None
    )
    item = next(
        iter(payload.customs.commodities if payload.customs is not None else []), None
    )
    payer: models.Address = (
        {
            provider_units.PaymentType.sender: payload.shipper,
            provider_units.PaymentType.recipient: payload.recipient,
            provider_units.PaymentType.third_party: payload.recipient,
        }.get(provider_units.PaymentType[payload.payment.paid_by])
        if payload.payment
        else None
    )

    request = Freightcom(
        username=settings.username,
        password=settings.password,
        version="3.1.0",
        ShippingRequest=ShippingRequestType(
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
            insuranceType=(options.insurance.state is not None),
            scheduledShipDate=None,
            insideDelivery=options.freightcom_inside_delivery.state,
            isSaturdayService=options.freightcom_is_saturday_service.state,
            dangerousGoodsType=options.freightcom_dangerous_goods_type.state,
            serviceId=service,
            stackable=options.freightcom_stackable.state,
            From=FromType(
                id=None,
                company=payload.shipper.company_name,
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
                company=payload.recipient.company_name,
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
            COD=(
                CODType(
                    paymentType=provider_units.PaymentType.recipient.value,
                    CODReturnAddress=CODReturnAddressType(
                        codCompany=payload.recipient.company_name,
                        codName=payload.recipient.person_name,
                        codAddress1=lib.join(
                            payload.recipient.address_line1, join=True
                        ),
                        codCity=payload.recipient.city,
                        codStateCode=payload.recipient.state_code,
                        codZip=payload.recipient.postal_code,
                        codCountry=payload.recipient.country_code,
                    ),
                )
                if options.cash_on_delivery.state is not None
                else None
            ),
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
            Payment=(
                RequestPaymentType(type_=payment_type)
                if payload.payment is not None
                else None
            ),
            Reference=(
                [ReferenceType(name="REF", code=payload.reference)]
                if payload.reference != ""
                else None
            ),
            CustomsInvoice=(
                CustomsInvoiceType(
                    BillTo=BillToType(
                        company=payer.company_name,
                        name=payer.person_name,
                        address1=lib.join(payer.address_line1, join=True),
                        city=payer.city,
                        state=payer.state_code,
                        zip=payer.postal_code,
                        country=payer.country_code,
                    ),
                    Contact=ContactType(
                        name=payer.person_name, phone=payer.phone_number
                    ),
                    Item=ItemType(
                        code=item.sku,
                        description=item.description,
                        originCountry=item.origin_country,
                        unitPrice=item.value_amount,
                    ),
                )
                if all([payload.customs, payer])
                else None
            ),
        ),
    )

    return lib.Serializable(request, provider_utils.standard_request_serializer)
