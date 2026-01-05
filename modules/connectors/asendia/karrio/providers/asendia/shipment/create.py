"""Karrio Asendia shipment API implementation."""

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.asendia.error as error
import karrio.providers.asendia.utils as provider_utils
import karrio.providers.asendia.units as provider_units
import karrio.schemas.asendia.shipment_request as asendia_req
import karrio.schemas.asendia.shipment_response as asendia_res


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[models.ShipmentDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Parse response to typed object
    shipment = lib.to_object(asendia_res.ShipmentResponseType, response)

    # Check if we have a valid shipment (tracking number present)
    has_shipment = shipment.trackingNumber is not None and len(messages) == 0

    details = _extract_details(shipment, settings, _response.ctx) if has_shipment else None

    return details, messages


def _extract_details(
    shipment: asendia_res.ShipmentResponseType,
    settings: provider_utils.Settings,
    ctx: dict = None,
) -> models.ShipmentDetails:
    """Extract shipment details from Asendia response."""
    ctx = ctx or {}
    label_type = ctx.get("label_type", "PDF")

    # Get label from context if proxy fetched it
    label = ctx.get("label")

    # Build documents
    docs = models.Documents(label=label) if label else None

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.trackingNumber,
        shipment_identifier=shipment.id,
        label_type=label_type,
        docs=docs,
        meta=dict(
            label_location=shipment.labelLocation,
            return_label_location=shipment.returnLabelLocation,
            return_tracking_number=shipment.returnTrackingNumber,
            customs_document_location=shipment.customsDocumentLocation,
            commercial_invoice_location=shipment.commercialInvoiceLocation,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a shipment request for Asendia API."""

    # Convert karrio models to carrier-specific format
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Get package (Asendia supports single package per request)
    package = packages.single

    # Parse service code (format: PRODUCT or PRODUCT_SERVICE)
    service_code = payload.service or "EPAQSTD"
    service_parts = service_code.split("_") if "_" in service_code else [service_code]
    product_code = service_parts[0]
    service_modifier = service_parts[1] if len(service_parts) > 1 else None

    # Determine label type
    label_type = provider_units.LabelType.map(
        payload.label_type or "PDF"
    ).value_or_key

    # Determine packaging format
    packaging_type = provider_units.PackagingType.map(
        package.packaging_type or "your_packaging"
    ).value_or_key

    # Build customs info for international shipments
    customs = payload.customs or models.Customs()
    customs_info = None

    if customs.commodities:
        customs_info = asendia_req.CustomsInfoType(
            currency=customs.duty.currency if customs.duty else "USD",
            items=[
                asendia_req.ItemType(
                    articleDescription=item.description or item.title,
                    articleNumber=item.sku,
                    unitValue=item.value_amount,
                    currency=item.value_currency or "USD",
                    harmonizationCode=item.hs_code,
                    originCountry=item.origin_country,
                    unitWeight=item.weight,
                    quantity=item.quantity or 1,
                )
                for item in customs.commodities
            ],
        )

    # Build return label option if requested
    return_label_option = None
    if options.asendia_return_label.state:
        return_label_option = asendia_req.ReturnLabelOptionType(
            enabled=True,
            type=options.asendia_return_label_type.state or "EPAQRETDOM",
            payment=options.asendia_return_label_payment.state or "RETPP",
        )

    # Build the request
    request = asendia_req.ShipmentRequestType(
        customerId=settings.customer_id,
        labelType=label_type,
        referencenumber=payload.reference,
        weight=package.weight.KG,
        shippingCost=options.declared_value.state if options.declared_value.state else None,
        senderEORI=options.asendia_sender_eori.state,
        sellerEORI=options.asendia_seller_eori.state,
        senderTaxId=options.asendia_sender_tax_id.state,
        receiverTaxId=options.asendia_receiver_tax_id.state,
        asendiaService=asendia_req.AsendiaServiceType(
            format=packaging_type,
            product=product_code,
            service=service_modifier,
            insurance=options.asendia_insurance.state,
            returnLabelOption=return_label_option,
        ),
        addresses=asendia_req.AddressesType(
            sender=asendia_req.ImporterType(
                name=shipper.person_name,
                company=shipper.company_name,
                address1=shipper.address_line1,
                address2=shipper.address_line2,
                city=shipper.city,
                province=shipper.state_code,
                postalCode=shipper.postal_code,
                country=shipper.country_code,
                email=shipper.email,
                phone=shipper.phone_number,
            ),
            receiver=asendia_req.ImporterType(
                name=recipient.person_name,
                company=recipient.company_name,
                address1=recipient.address_line1,
                address2=recipient.address_line2,
                city=recipient.city,
                province=recipient.state_code,
                postalCode=recipient.postal_code,
                country=recipient.country_code,
                email=recipient.email,
                phone=recipient.phone_number,
            ),
        ),
        customsInfo=customs_info,
    )

    return lib.Serializable(
        request,
        lib.to_dict,
        dict(label_type=label_type),
    )
