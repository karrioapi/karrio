"""Karrio Asendia shipment API implementation."""

import uuid

import karrio.core.models as models
import karrio.core.units as units
import karrio.lib as lib
import karrio.providers.asendia.error as error
import karrio.providers.asendia.units as provider_units
import karrio.providers.asendia.utils as provider_utils
import karrio.schemas.asendia.shipment_request as asendia_req
import karrio.schemas.asendia.shipment_response as asendia_res


def parse_shipment_response(
    _response: lib.Deserializable[list[tuple[dict, str]]],
    settings: provider_utils.Settings,
) -> tuple[models.ShipmentDetails | None, list[models.Message]]:
    """Parse shipment response from Asendia API.

    Asendia uses per-package requests (Pattern B), like Canada Post.
    Proxy fetches labels for each parcel, so we can use lib.to_multi_piece_shipment().
    Response format: [(parcel_dict, label_base64), ...]
    """
    responses = _response.deserialize()

    # Aggregate errors from all responses using sum()
    messages: list[models.Message] = sum(
        [error.parse_error_response(parcel, settings) for parcel, _ in responses],
        start=[],
    )

    # Extract shipment details from each valid response
    shipment = lib.to_multi_piece_shipment(
        [
            (
                f"{idx}",
                _extract_details(parcel, label, settings, _response.ctx),
            )
            for idx, (parcel, label) in enumerate(responses, start=1)
            if parcel.get("trackingNumber")
        ]
    )

    return shipment, messages


def _extract_details(
    data: dict,
    label: str | None,
    settings: provider_utils.Settings,
    ctx: dict = None,
) -> models.ShipmentDetails:
    """Extract shipment details from Asendia response."""
    shipment = lib.to_object(asendia_res.ShipmentResponseType, data)
    ctx = ctx or {}
    label_type = ctx.get("label_type", "PDF")

    # Label is fetched by proxy and passed directly
    docs = models.Documents(label=label)

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.trackingNumber,
        shipment_identifier=shipment.id,
        label_type=label_type,
        docs=docs,
        meta=dict(
            carrier_tracking_link=settings.tracking_url.format(shipment.trackingNumber),
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
    """Create a shipment request for Asendia API.

    Asendia uses per-package requests (Pattern B).
    Returns a list of requests, one per package.
    """
    # Convert karrio models to carrier-specific format
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Map karrio service to Asendia product code (e.g. "asendia_epaq_standard" -> "EPAQSTD")
    product_code = provider_units.ShippingService.map(payload.service or "EPAQSTD").value_or_key

    # AsendiaService.service is a mandatory API field (CUP/CPPR/CPPS for outbound, RETPP/RETPAP for returns).
    # User may override via asendia_service_type option; otherwise default based on product family.
    service_modifier = options.asendia_service_type.state or ("RETPP" if product_code.startswith("EPAQRET") else "CUP")

    # Determine label type
    label_type = provider_units.LabelType.map(payload.label_type or "PDF").value_or_key

    # Build customs info for international shipments using lib.to_customs_info
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit=units.WeightUnit.KG.name,
    )

    # Build return label option if requested
    is_domestic = shipper.country_code == recipient.country_code
    default_return_type = "EPAQRETDOM" if is_domestic else "EPAQRETINT"
    return_label_option = lib.identity(
        asendia_req.ReturnLabelOptionType(
            enabled=True,
            type=options.asendia_return_label_type.state or default_return_type,
            payment=options.asendia_return_label_payment.state or "RETPP",
        )
        if options.asendia_return_label.state
        else None
    )

    # Build list of requests, one per package (Pattern B: Per-Package Request)
    request = [
        asendia_req.ShipmentRequestType(
            customerId=settings.customer_id,
            labelType=label_type,
            referencenumber=(payload.reference or payload.order_id or uuid.uuid4().hex),
            weight=package.weight.KG,
            shippingCost=options.declared_value.state if options.declared_value.state else None,
            senderEORI=options.asendia_sender_eori.state,
            sellerEORI=options.asendia_seller_eori.state,
            senderTaxId=options.asendia_sender_tax_id.state,
            receiverTaxId=options.asendia_receiver_tax_id.state,
            asendiaService=asendia_req.AsendiaServiceType(
                format=provider_units.PackagingType.map(package.packaging_type or "your_packaging").value_or_key,
                product=product_code,
                service=service_modifier,
                insurance=options.asendia_insurance.state,
                returnLabelOption=return_label_option,
            ),
            addresses=asendia_req.AddressesType(
                sender=asendia_req.ImporterType(
                    name=lib.text(shipper.person_name, max=50),
                    company=lib.text(shipper.company_name, max=50),
                    address1=lib.text(shipper.address_line1, max=50),
                    address2=shipper.address_line2,
                    city=shipper.city,
                    province=shipper.state_code,
                    postalCode=shipper.postal_code,
                    country=shipper.country_code,
                    email=shipper.email,
                    phone=shipper.phone_number,
                ),
                receiver=asendia_req.ImporterType(
                    name=lib.text(recipient.person_name, max=50),
                    company=lib.text(recipient.company_name, max=50),
                    address1=lib.text(recipient.address_line1, max=50),
                    address2=recipient.address_line2,
                    city=recipient.city,
                    province=recipient.state_code,
                    postalCode=recipient.postal_code,
                    country=recipient.country_code,
                    email=recipient.email,
                    phone=recipient.phone_number,
                ),
            ),
            customsInfo=lib.identity(
                asendia_req.CustomsInfoType(
                    currency=lib.failsafe(lambda: customs.duty.currency) or "EUR",
                    items=[
                        asendia_req.ItemType(
                            articleDescription=lib.text(item.description or item.title, max=150),
                            articleNumber=item.sku,
                            unitValue=item.value_amount,
                            currency=item.value_currency or "EUR",
                            harmonizationCode=item.hs_code,
                            originCountry=item.origin_country,
                            unitWeight=item.weight,
                            quantity=item.quantity or 1,
                        )
                        for item in (package.items if any(package.items) else customs.commodities)
                    ],
                )
                if any(package.items) or customs.commodities
                else None
            ),
        )
        for package in packages
    ]

    return lib.Serializable(
        request,
        lib.to_dict,
        dict(label_type=label_type),
    )
