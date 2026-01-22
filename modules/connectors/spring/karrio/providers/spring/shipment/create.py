"""Karrio Spring shipment API implementation."""

import karrio.schemas.spring.shipment_request as spring_req
import karrio.schemas.spring.shipment_response as spring_res

import uuid
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.spring.error as error
import karrio.providers.spring.utils as provider_utils
import karrio.providers.spring.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[typing.List[dict]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[models.ShipmentDetails], typing.List[models.Message]]:
    """Parse shipment responses from Spring API.

    Spring is a per-package carrier, so we receive a list of responses
    (one per package) and aggregate them using lib.to_multi_piece_shipment().
    """
    responses = _response.deserialize()

    # Collect all error messages from all responses
    messages: typing.List[models.Message] = sum(
        [error.parse_error_response(response, settings) for response in responses],
        start=[],
    )

    # Extract shipment details for successful responses
    shipment_details = [
        (
            f"{index}",
            (
                _extract_details(response, settings)
                if response.get("Shipment") and response.get("ErrorLevel") in (0, 1)
                else None
            ),
        )
        for index, response in enumerate(responses, start=1)
    ]

    # Aggregate multi-piece shipment
    shipment = lib.to_multi_piece_shipment(shipment_details)

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    """Extract shipment details from Spring API response."""
    response = lib.to_object(spring_res.ShipmentResponseType, data)
    shipment = response.Shipment

    # Get tracking number - used as shipment_identifier for cancel operations
    tracking_number = shipment.TrackingNumber

    # Get label data - label_format defaults to PDF if not specified
    label_format = shipment.LabelFormat or "PDF"

    # Build documents object
    documents = models.Documents(label=shipment.LabelImage)

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=tracking_number,
        label_type=label_format,
        docs=documents,
        meta=dict(
            service=shipment.Service,
            carrier=shipment.Carrier,
            shipper_reference=shipment.ShipperReference,
            carrier_tracking_number=shipment.CarrierTrackingNumber,
            carrier_local_tracking_number=shipment.CarrierLocalTrackingNumber,
            carrier_tracking_url=shipment.CarrierTrackingUrl,
            display_id=shipment.DisplayId,
            label_type=shipment.LabelType,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create Spring OrderShipment requests.

    Spring is a per-package carrier, so we create one request per package
    and return a list of requests to be processed in parallel.
    """
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Get customs info for international shipments
    customs = lib.to_customs_info(
        payload.customs,
        shipper=shipper,
        recipient=recipient,
        weight_unit=units.WeightUnit.KG.name,
    )

    # Determine label format from settings or payload
    label_format = (
        provider_units.LabelFormat.map(payload.label_type).value
        or settings.connection_config.label_format.state
        or "PDF"
    )

    # Build consignor (shipper) address (same for all packages)
    consignor_address = spring_req.ConsignorAddressType(
        Name=shipper.person_name or shipper.company_name,
        Company=shipper.company_name,
        AddressLine1=shipper.address_line1,
        AddressLine2=shipper.address_line2,
        AddressLine3=None,
        City=shipper.city,
        State=shipper.state_code,
        Zip=shipper.postal_code,
        Country=shipper.country_code,
        Phone=shipper.phone_number,
        Email=shipper.email,
        Vat=options.spring_consignor_vat.state or shipper.tax_id,
        Eori=options.spring_consignor_eori.state,
        NlVat=options.spring_consignor_nl_vat.state,
        EuEori=options.spring_consignor_eu_eori.state,
        GbEori=options.spring_consignor_gb_eori.state,
        Ioss=options.spring_consignor_ioss.state,
        LocalTaxNumber=options.spring_consignor_local_tax_number.state,
    )

    # Build consignee (recipient) address (same for all packages)
    consignee_address = spring_req.AddressType(
        Name=recipient.person_name or recipient.company_name,
        Company=recipient.company_name,
        AddressLine1=recipient.address_line1,
        AddressLine2=recipient.address_line2,
        AddressLine3=None,
        City=recipient.city,
        State=recipient.state_code,
        Zip=recipient.postal_code,
        Country=recipient.country_code,
        Phone=recipient.phone_number,
        Email=recipient.email,
        Vat=recipient.tax_id,
        PudoLocationId=options.spring_pudo_location_id.state,
    )

    # Build products array (customs items) - same for all packages
    products = [
        spring_req.ProductType(
            Description=lib.text(item.description or item.title, max=60),
            Sku=item.sku,
            HsCode=item.hs_code,
            OriginCountry=item.origin_country or shipper.country_code,
            Quantity=str(item.quantity or 1),
            Value=str(item.value_amount or 0),
            Weight=str(item.weight or 0),
        )
        for item in (customs.commodities if customs else [])
    ]

    # Calculate total value from products or use declared value
    total_value = (
        sum(float(p.Value or 0) for p in products)
        if products
        else (customs.duty.declared_value if customs and customs.duty else None)
    )

    # Get declaration type mapping
    declaration_type = None
    if customs and customs.content_type:
        declaration_type = provider_units.CustomsContentType.map(
            customs.content_type
        ).value

    # Get customs duty type
    customs_duty = options.spring_customs_duty.state or (
        provider_units.CustomsDuty.map(customs.incoterm).value
        if customs and customs.incoterm
        else "DDU"
    )

    # Generate base reference for multi-piece shipment
    base_reference = payload.reference or str(uuid.uuid4().hex)

    # Create one request per package
    requests = [
        spring_req.ShipmentRequestType(
            Apikey=settings.api_key,
            Command="OrderShipment",
            Shipment=spring_req.ShipmentType(
                LabelFormat=label_format,
                # Append package index to reference for multi-piece tracking
                ShipperReference=(
                    f"{base_reference}-{index + 1}"
                    if len(packages) > 1
                    else base_reference
                ),
                OrderReference=options.spring_order_reference.state,
                OrderDate=options.spring_order_date.state,
                DisplayId=options.spring_display_id.state,
                InvoiceNumber=options.spring_invoice_number.state,
                Service=service,
                Weight=str(package.weight.KG),
                WeightUnit="kg",
                Length=str(package.length.CM) if package.length.CM else None,
                Width=str(package.width.CM) if package.width.CM else None,
                Height=str(package.height.CM) if package.height.CM else None,
                DimUnit="cm" if any([package.length.CM, package.width.CM, package.height.CM]) else None,
                Value=str(total_value) if total_value else None,
                ShippingValue=str(options.spring_shipping_value.state) if options.spring_shipping_value.state else None,
                Currency=customs.duty.currency if customs and customs.duty else options.currency.state,
                CustomsDuty=customs_duty,
                Description=package.parcel.description or (customs.content_description if customs else None),
                DeclarationType=declaration_type or options.spring_declaration_type.state,
                DangerousGoods="Y" if options.spring_dangerous_goods.state else "N",
                ExportCarrierName=options.spring_export_carrier_name.state,
                ExportAwb=options.spring_export_awb.state,
                ConsignorAddress=consignor_address,
                ConsigneeAddress=consignee_address,
                # Pass empty list instead of None to avoid jstruct [None] serialization bug
                Products=products if products else [],
            ),
        )
        for index, package in enumerate(packages)
    ]

    return lib.Serializable(requests, lambda reqs: [lib.to_dict(r) for r in reqs])
