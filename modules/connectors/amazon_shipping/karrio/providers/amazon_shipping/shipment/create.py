"""Karrio Amazon Shipping shipment creation implementation."""

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.amazon_shipping.error as error
import karrio.providers.amazon_shipping.units as provider_units
import karrio.providers.amazon_shipping.utils as provider_utils
import karrio.schemas.amazon_shipping.one_click_shipment_response as amazon


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> tuple[models.ShipmentDetails, list[models.Message]]:
    """Parse shipment creation response from Amazon Shipping API. See SPECS.md."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    payload = response.get("payload") or {}

    shipment = _extract_details(payload, settings) if payload.get("shipmentId") else None

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    """Extract shipment details from API response payload."""
    result = lib.to_object(amazon.Payload, data)

    package_docs = result.packageDocumentDetails or []
    tracking_ids = [pkg.trackingId for pkg in package_docs if pkg.trackingId]

    labels = [
        doc.contents
        for pkg in package_docs
        for doc in (pkg.packageDocuments or [])
        if doc.type == "LABEL" and doc.contents
    ]

    label_format = next(
        (doc.format for pkg in package_docs for doc in (pkg.packageDocuments or []) if doc.type == "LABEL"),
        "PNG",
    )
    label = lib.bundle_base64(labels, label_format) if len(labels) > 1 else next(iter(labels), None)

    # PNG labels are normalised to PDF (see SPECS.md).
    if label and label_format == "PNG":
        label = lib.image_to_pdf(label)
        label_format = "PDF"

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=next(iter(tracking_ids), None),
        shipment_identifier=result.shipmentId,
        label_type=label_format,
        docs=models.Documents(label=label),
        meta=dict(
            shipment_id=result.shipmentId,
            tracking_numbers=tracking_ids,
            carrier_id=lib.failsafe(lambda: result.carrier.id),
            carrier_name=lib.failsafe(lambda: result.carrier.name),
            service_id=lib.failsafe(lambda: result.service.id),
            service_name=lib.failsafe(lambda: result.service.name),
            total_charge=lib.failsafe(lambda: lib.to_money(result.totalCharge.value)),
            currency=lib.failsafe(lambda: result.totalCharge.unit),
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create Amazon Shipping shipment request using oneClickShipment API."""
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels, required=["weight"])
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    label_format = options.amazon_shipping_label_format.state or settings.connection_config.label_format.state or "PNG"

    request = dict(
        shipFrom=dict(
            name=shipper.company_name or shipper.person_name,
            addressLine1=shipper.street,
            addressLine2=shipper.address_line2,
            addressLine3=None,
            companyName=shipper.company_name,
            stateOrRegion=shipper.state_code,
            city=shipper.city,
            countryCode=shipper.country_code,
            postalCode=shipper.postal_code,
            email=shipper.email,
            phoneNumber=shipper.phone_number,
        ),
        shipTo=dict(
            name=recipient.company_name or recipient.person_name,
            addressLine1=recipient.street,
            addressLine2=recipient.address_line2,
            addressLine3=None,
            companyName=recipient.company_name,
            stateOrRegion=recipient.state_code,
            city=recipient.city,
            countryCode=recipient.country_code,
            postalCode=recipient.postal_code,
            email=recipient.email,
            phoneNumber=recipient.phone_number,
        ),
        shipDate=lib.fdatetime(
            options.shipment_date.state,
            current_format="%Y-%m-%d",
            output_format="%Y-%m-%dT%H:%M:%SZ",
        )
        if options.shipment_date.state
        else None,
        packages=[
            dict(
                dimensions=dict(
                    length=package.length.IN,
                    width=package.width.IN,
                    height=package.height.IN,
                    unit="INCH",
                )
                if package.has_dimensions
                else None,
                weight=dict(
                    value=package.weight.LB,
                    unit="POUND",
                ),
                # insuredValue and items are required by the v2 spec (see SPECS.md).
                insuredValue=dict(
                    value=lib.to_money(package.options.declared_value.state or 0),
                    unit=package.options.currency.state or "USD",
                ),
                items=[
                    dict(
                        quantity=item.quantity or 1,
                        description=item.description,
                        itemIdentifier=item.sku or item.hs_code,
                        weight=dict(
                            value=item.weight,
                            unit="POUND",
                        )
                        if item.weight
                        else None,
                        itemValue=dict(
                            value=lib.to_money(item.value_amount),
                            unit=item.value_currency or "USD",
                        )
                        if item.value_amount
                        else None,
                    )
                    for item in (package.items or [])
                ],
                packageClientReferenceId=package.parcel.id or str(index),
            )
            for index, package in enumerate(packages, 1)
        ],
        channelDetails=dict(
            channelType=options.amazon_shipping_channel_type.state or "EXTERNAL",
        ),
        labelSpecifications=dict(
            format=label_format,
            size=dict(
                length=settings.connection_config.label_size_length.state or 6,
                width=settings.connection_config.label_size_width.state or 4,
                unit=settings.connection_config.label_size_unit.state or "INCH",
            ),
            dpi=300,
            pageLayout="DEFAULT",
            needFileJoining=len(packages) > 1,
            requestedDocumentTypes=["LABEL"],
        ),
        serviceSelection=dict(
            serviceId=[service] if service else None,
        )
        if service
        else None,
        shipperInstruction=dict(
            deliveryNotes=options.delivery_instructions.state,
        )
        if options.delivery_instructions.state
        else None,
    )

    return lib.Serializable(request, lib.to_dict)
