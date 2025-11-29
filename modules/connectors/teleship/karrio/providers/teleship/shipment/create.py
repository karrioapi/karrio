"""Karrio Teleship shipment API implementation."""

import karrio.schemas.teleship.shipment_request as teleship_req
import karrio.schemas.teleship.shipment_response as teleship_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.teleship.error as error
import karrio.providers.teleship.utils as provider_utils
import karrio.providers.teleship.units as provider_units


def parse_shipment_response(
    _responses: lib.Deserializable[typing.List[dict]],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    responses = _responses.deserialize()

    shipment = lib.to_multi_piece_shipment(
        [
            (
                f"{_}",
                (
                    _extract_details(response.get("shipment"), settings)
                    if response.get("shipment")
                    else None
                ),
            )
            for _, response in enumerate(responses, start=1)
        ]
    )
    messages: typing.List[models.Message] = sum(
        [error.parse_error_response(response, settings) for response in responses],
        start=[],
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    """Extract shipment details from carrier response data"""
    shipment = lib.to_object(teleship_res.ShipmentType, data)
    service = provider_units.ShippingService.map(shipment.rate.service.code)

    # Extract label document from documents array
    label = lib.identity(
        next(
            (doc for doc in (shipment.documents or []) if doc.type == "LABEL"),
            None,
        )
    )
    invoice = lib.identity(
        next(
            (doc for doc in (shipment.documents or []) if doc.type == "INVOICE"),
            None,
        )
    )

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.trackingNumber,
        shipment_identifier=shipment.shipmentId,
        label_type=label.format or "PDF",
        docs=models.Documents(
            label=getattr(label, "base64String", None),
            invoice=getattr(invoice, "base64String", None),
        ),
        selected_rate=models.RateDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            service=service.name_or_key,
            total_charge=lib.to_money(shipment.rate.price),
            currency=shipment.rate.currency,
            transit_days=shipment.rate.transit,
            estimated_delivery=lib.fdate(
                shipment.rate.estimatedDelivery,
                try_formats=["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"],
            ),
            extra_charges=[
                models.ChargeDetails(
                    name=charge.name,
                    amount=lib.to_money(charge.amount),
                    currency=charge.currency,
                )
                for charge in shipment.rate.charges
            ],
            meta=dict(
                service_name=service.name_or_key,
            ),
        ),
        meta=dict(
            customer_reference=shipment.customerReference,
            service_name=service.name_or_key,
            ship_date=shipment.shipDate,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a shipment request for the carrier API"""
    # Convert karrio models using functional lib utilities
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    billing_address = lib.to_address(payload.billing_address)
    return_address = lib.to_address(payload.return_address)
    is_intl = payload.recipient.country_code != payload.shipper.country_code

    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        initializer=provider_units.shipping_options_initializer,
    )
    packages = lib.to_packages(
        payload.parcels,
        options=options,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit=units.WeightUnit.KG.name,
    )

    # Build request using typed schema classes
    request = [
        teleship_req.ShipmentRequestType(
            serviceCode=service,
            customerReference=payload.reference,
            description=package.parcel.description,
            shipDate=options.shipping_date.state,
            orderTrackingReference=options.teleship_order_tracking_reference.state,
            commercialInvoiceReference=customs.invoice,
            packageType=provider_units.PackagingType.map(
                package.packaging_type or "your_packaging"
            ).value_or_key,
            shipTo=teleship_req.BillToType(
                name=recipient.contact or "N/A",
                company=recipient.company_name,
                email=recipient.email,
                phone=recipient.phone_number,
                address=teleship_req.AddressType(
                    line1=recipient.address_line1,
                    line2=recipient.address_line2,
                    city=recipient.city,
                    state=recipient.state_code,
                    postcode=recipient.postal_code,
                    country=recipient.country_code,
                ),
            ),
            shipFrom=teleship_req.BillToType(
                name=shipper.contact or "N/A",
                company=shipper.company_name,
                email=shipper.email,
                phone=shipper.phone_number,
                address=teleship_req.AddressType(
                    line1=shipper.address_line1,
                    line2=shipper.address_line2,
                    city=shipper.city,
                    state=shipper.state_code,
                    postcode=shipper.postal_code,
                    country=shipper.country_code,
                ),
            ),
            returnTo=lib.identity(
                teleship_req.BillToType(
                    name=return_address.contact or "N/A",
                    company=return_address.company_name,
                    email=return_address.email,
                    phone=return_address.phone_number,
                    address=teleship_req.AddressType(
                        line1=return_address.address_line1,
                        line2=return_address.address_line2,
                        city=return_address.city,
                        state=return_address.state_code,
                        postcode=return_address.postal_code,
                        country=return_address.country_code,
                    ),
                )
                if payload.return_address
                else None
            ),
            billTo=lib.identity(
                teleship_req.BillToType(
                    name=billing_address.contact or "N/A",
                    company=billing_address.company_name,
                    email=billing_address.email,
                    phone=billing_address.phone_number,
                    address=teleship_req.AddressType(
                        line1=billing_address.address_line1,
                        line2=billing_address.address_line2,
                        city=billing_address.city,
                        state=billing_address.state_code,
                        postcode=billing_address.postal_code,
                        country=billing_address.country_code,
                    ),
                    stateTaxId=billing_address.state_tax_id,
                    countryTaxId=billing_address.federal_tax_id,
                )
                if payload.billing_address
                else None
            ),
            weight=teleship_req.WeightType(
                value=package.weight.value,
                unit=package.weight.unit.lower(),
            ),
            dimensions=lib.identity(
                teleship_req.DimensionsType(
                    unit=package.dimension_unit.lower(),
                    length=package.length.value,
                    width=package.width.value,
                    height=package.height.value,
                )
                if all(
                    [
                        package.length.value,
                        package.width.value,
                        package.height.value,
                    ]
                )
                else None
            ),
            additionalServices=lib.identity(
                teleship_req.AdditionalServicesType(
                    signatureRequired=options.teleship_signature_required.state,
                    deliveryWarranty=options.teleship_delivery_warranty.state,
                    deliveryPUDO=options.teleship_delivery_pudo.state,
                    lowCarbon=options.teleship_low_carbon.state,
                    dutyTaxCalculation=options.teleship_duty_tax_calculation.state,
                )
                if any(
                    [
                        options.teleship_signature_required.state,
                        options.teleship_delivery_warranty.state,
                        options.teleship_delivery_pudo.state,
                        options.teleship_low_carbon.state,
                        options.teleship_duty_tax_calculation.state,
                    ]
                )
                else None
            ),
            commodities=[
                teleship_req.CommodityType(
                    sku=commodity.sku,
                    hsCode=commodity.hs_code,
                    title=lib.text(commodity.title or commodity.description, max=200),
                    description=lib.text(
                        commodity.description if commodity.title else None, max=200
                    ),
                    category=commodity.category,
                    value=teleship_req.ValueType(
                        amount=commodity.value_amount,
                        currency=commodity.value_currency,
                    ),
                    quantity=commodity.quantity,
                    unitWeight=teleship_req.WeightType(
                        value=commodity.weight,
                        unit=commodity.weight_unit.lower(),
                    ),
                    countryOfOrigin=commodity.origin_country,
                    imageUrl=commodity.image_url,
                    productUrl=commodity.product_url,
                    compliance=None,
                )
                for commodity in (
                    package.items if any(package.items) else customs.commodities or []
                )
            ],
            customs=lib.identity(
                teleship_req.CustomsType(
                    EORI=customs.options.eori_number.state,
                    IOSS=customs.options.ioss.state,
                    VAT=customs.options.vat.state,
                    EIN=customs.options.ein.state,
                    VOECNUMBER=customs.options.voec_number.state,
                    importerGST=customs.options.importer_gst.state,
                    exporterGST=customs.options.exporter_gst.state,
                    consigneeGST=customs.options.consignee_gst.state,
                    contentType=provider_units.CustomsContentType.map(
                        customs.content_type or "other"
                    ).value,
                    invoiceDate=customs.invoice_date,
                    invoiceNumber=customs.invoice,
                    GPSRContactInfo=options.teleship_gpsr_contact_info.state,
                    importerOfRecord=lib.identity(
                        teleship_req.BillToType(
                            name=customs.duty_billing_address.contact or "N/A",
                            company=customs.duty_billing_address.company_name,
                            email=customs.duty_billing_address.email,
                            phone=customs.duty_billing_address.phone_number,
                            address=teleship_req.AddressType(
                                line1=customs.duty_billing_address.address_line1,
                                line2=customs.duty_billing_address.address_line2,
                                city=customs.duty_billing_address.city,
                                state=customs.duty_billing_address.state_code,
                                country=customs.duty_billing_address.country_code,
                                postcode=customs.duty_billing_address.postal_code,
                            ),
                            stateTaxId=customs.duty_billing_address.state_tax_id,
                            countryTaxId=customs.duty_billing_address.federal_tax_id,
                        )
                        if payload.customs.duty_billing_address
                        else None
                    ),
                )
                if payload.customs and is_intl
                else None
            ),
        )
        for package in packages
    ]

    return lib.Serializable(request, lib.to_dict)
