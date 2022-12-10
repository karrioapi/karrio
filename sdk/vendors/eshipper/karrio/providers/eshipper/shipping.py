from eshipper_lib.shipping_request import (
    EShipper,
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
    DutiesTaxesType,
)
from eshipper_lib.shipping_reply import (
    ShippingReplyType,
    QuoteType,
)

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.eshipper.error as provider_error
import karrio.providers.eshipper.units as provider_units
import karrio.providers.eshipper.utils as provider_utils


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
    node: lib.Element, settings: provider_utils.Settings
) -> models.ShipmentDetails:
    shipping = lib.to_object(ShippingReplyType, node)
    quote: QuoteType = shipping.Quote

    tracking_number = getattr(
        next(iter(shipping.Package), None), "trackingNumber", None
    )
    rate_provider, service, service_name = provider_units.ShippingService.info(
        quote.serviceId,
        quote.carrierId,
        quote.serviceName,
        quote.carrierName,
    )
    invoice = dict(invoice=shipping.CustomsInvoice) if shipping.CustomsInvoice else {}
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
            if quote is not None
            else None
        ),
        docs=models.Documents(label=shipping.Labels, **invoice),
        meta=dict(
            rate_provider=rate_provider,
            service_name=service_name,
            tracking_url=shipping.TrackingURL,
        ),
    )


def shipping_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable[EShipper]:
    service = provider_units.ShippingService.map(payload.service).value_or_key
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

    payment = payload.payment or models.Payment()
    is_intl = payload.shipper.country_code != payload.recipient.country_code
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit=packages.weight_unit,
        default_to=(
            models.Customs(
                commodities=(
                    packages.items
                    if any(packages.items)
                    else [
                        models.Commodity(
                            quantity=1,
                            sku=f"000{index}",
                            weight=pkg.weight.value,
                            weight_unit=pkg.weight_unit.value,
                            description=pkg.parcel.content,
                        )
                        for index, pkg in enumerate(packages, start=1)
                    ]
                )
            )
            if is_intl
            else None
        ),
    )

    packaging_type = provider_units.PackagingType[
        packages.package_type or "eshipper_boxes"
    ].value
    packaging = (
        "Pallet"
        if packaging_type in [provider_units.PackagingType.pallet.value]
        else "Package"
    )
    payment_type = (
        provider_units.PaymentType[payment.paid_by].value if payload.payment else None
    )

    request = EShipper(
        username=settings.username,
        password=settings.password,
        version="3.0.0",
        ShippingRequest=ShippingRequestType(
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
            serviceId=service,
            stackable=options.eshipper_stackable.state,
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
            Payment=(RequestPaymentType(type_=payment_type) if payment_type else None),
            Reference=(
                [ReferenceType(name="REF", code=payload.reference)]
                if payload.reference != ""
                else None
            ),
            CustomsInvoice=(
                CustomsInvoiceType(
                    Currency=getattr(customs.duty, "currency", None),
                    brokerName=None,
                    contactCompany=customs.duty_billing_address.company_name,
                    shipperTaxID=customs.duty_billing_address.tax_id,
                    contactName=customs.duty_billing_address.person_name,
                    contactPhone=customs.duty_billing_address.phone_number,
                    DutiesTaxes=DutiesTaxesType(
                        consigneeAccount=customs.duty.account_number,
                        sedNumber=None,
                        dutiable=("No" if packages.is_document else "Yes"),
                        billTo=provider_units.DutyBillToType.map(
                            customs.duty.paid_by or "shipper"
                        ).value,
                    ),
                    InBondManifest=None,
                    BillTo=BillToType(
                        company=customs.duty_billing_address.company_name,
                        name=customs.duty_billing_address.person_name,
                        address1=customs.duty_billing_address.address_line,
                        city=customs.duty_billing_address.city,
                        state=customs.duty_billing_address.state_code,
                        zip=customs.duty_billing_address.postal_code,
                        country=customs.duty_billing_address.country_code,
                    ),
                    Contact=ContactType(
                        name=customs.duty_billing_address.person_name,
                        phone=customs.duty_billing_address.phone_number,
                    ),
                    Item=[
                        ItemType(
                            code=item.hs_code or "0000",
                            description=item.description or "item",
                            originCountry=item.origin_country
                            or payload.shipper.country_code,
                            unitPrice=item.value_amount,
                            quantity=item.quantity or 1,
                            skuCode=item.sku,
                        )
                        for item in customs.commodities
                    ],
                )
                if payload.customs
                else None
            ),
        ),
    )

    return lib.Serializable(request, provider_utils.standard_request_serializer)
