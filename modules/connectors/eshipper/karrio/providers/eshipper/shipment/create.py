import karrio.schemas.eshipper.shipping_request as eshipper
import karrio.schemas.eshipper.shipping_response as shipping
import typing
import datetime
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.eshipper.error as error
import karrio.providers.eshipper.utils as provider_utils
import karrio.providers.eshipper.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    shipment = _extract_details(response, settings) if "order" in response else None

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    shipment = lib.to_object(shipping.ShippingResponseType, data)
    label_type = next((_.type for _ in shipment.labelData.label), "PDF").upper()
    label = lib.bundle_base64([_.data for _ in shipment.labelData.label], label_type)
    invoice = lib.failsafe(lambda: shipment.customsInvoice.data)
    trackingNumbers = [_.trackingNumber for _ in shipment.packages]
    service = provider_units.ShippingService.find(
        shipment.carrier.serviceName,
        test_mode=settings.test_mode,
    )
    rate_provider = provider_units.RateProvider.find(
        shipment.carrier.carrierName,
        test_mode=settings.test_mode,
    )

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.trackingNumber,
        shipment_identifier=shipment.order.id,
        label_type=label_type,
        docs=models.Documents(label=label, invoice=invoice),
        meta=lib.to_dict(
            dict(
                service_name=service.name_or_key,
                rate_provider=rate_provider.name_or_key,
                carrier_tracking_link=shipment.trackingUrl,
                tracking_numbers=trackingNumbers,
                orderId=shipment.order.id,
                transactionId=shipment.transactionId,
                billingReference=shipment.billingReference,
                eshipper_carrier_name=shipment.carrier.carrierName,
            )
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    is_intl = shipper.country_code != recipient.country_code

    payment = payload.payment or models.Payment()
    payor = lib.to_address(
        {
            "sender": payload.shipper,
            "recipient": payload.recipient,
            "thid_party": payload.billing_address,
        }.get(payment.paid_by)
    )
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
    service = provider_units.ShippingService.map(payload.service)
    service_id = lib.identity(
        options.eshipper_service_id.state
        or provider_units.ShippingService.service_id(
            service.name_or_key,
            test_mode=settings.test_mode,
        )
    )
    carrier_id = lib.identity(
        options.eshipper_carrier_id.state
        or provider_units.ShippingService.carrier_id(
            service.name_or_key,
            service_id=service_id,
            test_mode=settings.test_mode,
            service_search=service.name_or_key,
        )
    )

    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit=packages.weight_unit,
        default_to=lib.identity(
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

    request = eshipper.ShippingRequestType(
        scheduledShipDate=lib.fdatetime(
            lib.to_next_business_datetime(
                options.shipping_date.state or datetime.datetime.now(),
                current_format="%Y-%m-%dT%H:%M",
            ),
            output_format="%Y-%m-%d %H:%M",
        ),
        shippingrequestfrom=eshipper.FromType(
            attention=shipper.contact,
            company=shipper.company_name,
            address1=shipper.address_line1,
            address2=shipper.address_line2,
            city=shipper.city,
            province=shipper.state_code,
            country=shipper.country_code,
            zip=shipper.postal_code,
            email=shipper.email_address,
            phone=shipper.phone_number,
            instructions=None,
            residential=shipper.is_residential,
            tailgateRequired=None,
            confirmDelivery=None,
            notifyRecipient=None,
        ),
        to=eshipper.FromType(
            attention=recipient.contact,
            company=recipient.company_name,
            address1=recipient.address_line1,
            address2=recipient.address_line2,
            city=recipient.city,
            province=recipient.state_code,
            country=recipient.country_code,
            zip=recipient.postal_code,
            email=recipient.email_address,
            phone=recipient.phone_number,
            instructions=None,
            residential=recipient.is_residential,
            tailgateRequired=None,
            confirmDelivery=None,
            notifyRecipient=None,
        ),
        packagingUnit="Metric" if packages.weight_unit.lower() == "kg" else "Imperial",
        packages=eshipper.PackagesType(
            type="Package",
            packages=[
                eshipper.PackageType(
                    height=lib.to_int(package.height.value),
                    length=lib.to_int(package.length.value),
                    width=lib.to_int(package.width.value),
                    weight=lib.to_int(package.weight.value),
                    dimensionUnit=package.dimension_unit.value,
                    weightUnit=package.weight_unit.value,
                    type=provider_units.PackagingType.map(package.packaging_type).value,
                    freightClass=package.parcel.freight_class,
                    nmfcCode=None,
                    insuranceAmount=package.options.insurance.state,
                    codAmount=None,
                    description=package.description,
                    harmonizedCode=None,
                    skuCode=None,
                )
                for package in packages
            ],
        ),
        reference1=payload.reference,
        reference2=None,
        reference3=None,
        transactionId=None,
        signatureRequired=options.eshipper_signature_required.state,
        insuranceType=None,
        dangerousGoodsType=None,
        pickup=None,
        customsInformation=lib.identity(
            eshipper.CustomsInformationType(
                contact=eshipper.ContactType(
                    contactCompany=shipper.company_name,
                    contactName=shipper.contact,
                    brokerName=None,
                    brokerTaxId=None,
                    recipientTaxId=None,
                ),
                items=eshipper.ItemsType(
                    currency=(customs.duty.currency or options.currency.state),
                    items=[
                        eshipper.ItemType(
                            hsnCode=item.hs_code,
                            description=item.title or item.description,
                            originCountry=item.origin_country,
                            quantity=item.quantity,
                            unitPrice=lib.to_money(item.value_amount),
                            skuCode=item.sku,
                        )
                        for item in customs.commodities
                    ],
                ),
                dutiesTaxes=eshipper.DutiesTaxesType(
                    dutiable=not packages.is_document,
                    billTo=customs.duty_billing_address.contact,
                    accountNumber=customs.duty.account_number,
                    sedNumber=customs.options.sed_number.state,
                ),
                billingAddress=eshipper.BillingAddressType(
                    company=customs.duty_billing_address.company_name,
                    attention=customs.duty_billing_address.contact,
                    address1=customs.duty_billing_address.address_line1,
                    address2=customs.duty_billing_address.address_line2,
                    city=customs.duty_billing_address.city,
                    province=customs.duty_billing_address.state_code,
                    country=customs.duty_billing_address.country_code,
                    zip=customs.duty_billing_address.postal_code,
                    email=customs.duty_billing_address.email_address,
                    phone=customs.duty_billing_address.phone_number,
                ),
                remarks=None,
            )
            if payload.customs
            else None
        ),
        cod=lib.identity(
            eshipper.CodType(
                codAddress=eshipper.CodAddressType(
                    company=recipient.company_name,
                    name=recipient.contact,
                    city=recipient.city,
                    province=recipient.state_code,
                    country=recipient.country_code,
                    zip=recipient.postal_code,
                ),
                paymentType="Cash",
            )
            if options.cash_on_delivery.state
            else None
        ),
        isSaturdayService=options.eshipper_is_saturday_service.state,
        holdForPickupRequired=options.eshipper_hold_for_pickup_required.state,
        specialEquipment=options.eshipper_special_equipment.state,
        insideDelivery=options.eshipper_inside_delivery.state,
        deliveryAppointment=options.eshipper_delivery_appointment.state,
        insidePickup=options.eshipper_inside_pickup.state,
        saturdayPickupRequired=options.eshipper_saturday_pickup_required.state,
        stackable=options.eshipper_stackable.state,
        serviceId=service_id,
        thirdPartyBilling=lib.identity(
            eshipper.ThirdPartyBillingType(
                carrier=carrier_id,
                country=payor.country_code,
                billToAccountNumber=payment.account_number,
                billToPostalCode=payor.postal_code,
            )
            if payment.paid_by == "third_party"
            else None
        ),
        commodityType=customs.content_type,
    )

    return lib.Serializable(
        request,
        lambda _: lib.to_dict(lib.to_json(_).replace("shippingrequestfrom", "from")),
    )
