"""Karrio MyDHL shipment API implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract shipment details from the response
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., ShipmentRequestType),
# while XML schema types don't have this suffix (e.g., ShipmentRequest).

import karrio.schemas.mydhl.shipment_request as mydhl_req
import karrio.schemas.mydhl.shipment_response as mydhl_res

import time
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.mydhl.error as error
import karrio.providers.mydhl.utils as provider_utils
import karrio.providers.mydhl.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    shipment_response = lib.to_object(mydhl_res.ShipmentResponseType, response)

    details = _extract_details(shipment_response, settings)

    return details, messages


def _extract_details(
    shipment: mydhl_res.ShipmentResponseType,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    """
    Extract shipment details from MyDHL shipment response

    shipment: The MyDHL ShipmentResponseType object
    settings: The carrier connection settings

    Returns a ShipmentDetails object with extracted shipment information
    """
    # Extract tracking number (MyDHL returns as integer)
    tracking_number = str(shipment.shipmentTrackingNumber) if shipment.shipmentTrackingNumber else ""

    # Extract label document from documents array using functional pattern
    label_doc = next(
        (doc for doc in (shipment.documents or []) if doc and doc.content),
        None
    )

    # Get label content and format
    label = label_doc.content if label_doc else ""
    label_format = label_doc.imageFormat if label_doc else "PDF"

    # Extract package tracking numbers for metadata
    package_tracking_numbers = [
        pkg.trackingNumber
        for pkg in (shipment.packages or [])
        if pkg and pkg.trackingNumber
    ]

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=tracking_number,
        label_type=label_format,
        docs=models.Documents(label=label),
        meta=dict(
            tracking_url=shipment.trackingUrl if shipment.trackingUrl else "",
            package_tracking_numbers=package_tracking_numbers,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a shipment request for MyDHL API

    payload: The standardized ShipmentRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    # Convert karrio models to carrier-specific format
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    # Map service to DHL product code (e.g., "P", "T", "8")
    # Use .map() following FedEx, UPS, Canada Post pattern
    # Handles both service names ("mydhl_express_worldwide") and product codes ("P")
    service_code = provider_units.ShippingService.map(payload.service).value_or_key

    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Extract customs information for international shipments
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit=packages.weight_unit,
    )

    # Check if shipment is international (different countries)
    is_international = shipper.country_code != recipient.country_code

    # Calculate declared value for international shipments
    # Follow integration guide pattern: extract from customs, options, or packages
    declared_value = None
    declared_currency = None

    if is_international:
        # Get declared value from multiple sources (priority order)
        declared_value = (
            # First check customs duty declared value
            lib.to_money(customs.duty.declared_value) if customs and customs.duty else None
        ) or (
            # Then check options
            lib.to_money(options.declared_value.state) if options.declared_value.state else None
        ) or (
            # Then check customs commodities value
            lib.to_money(customs.commodities.value_amount) if customs and customs.commodities else None
        ) or (
            # Finally sum package values
            sum([lib.to_money(p.total_value or 0) for p in packages]) or 1.0
        )

        # Get currency from customs or options, default to USD
        declared_currency = (
            customs.duty.currency if customs and customs.duty else None
        ) or (
            options.currency.state if options.currency.state else None
        ) or "USD"

    # Build export declaration for international dutiable shipments
    # Required by DHL when isCustomsDeclarable=True
    export_declaration = None
    if is_international:
        # Use customs commodities if provided, otherwise create default from package data
        commodities_to_use = (
            customs.commodities
            if customs and customs.commodities
            else None
        )

        # Generate line items from commodities or create default from packages
        if commodities_to_use:
            # Use provided customs commodities
            line_items = [
                mydhl_req.LineItemType(
                    number=index,
                    description=lib.text(
                        item.description or item.title or "Commodity",
                        max=75
                    ),
                    price=int(item.value_amount or 0),
                    quantity=mydhl_req.QuantityType(
                        value=item.quantity,
                        unitOfMeasurement="PCS",
                    ),
                    commodityCodes=[
                        mydhl_req.CommodityCodeType(
                            typeCode="outbound",
                            value=int(item.hs_code[:6]) if item.hs_code else None,
                        )
                    ] if item.hs_code else None,
                    exportReasonType=(
                        "permanent"
                        if customs and customs.content_type in ["merchandise", "commercial_purpose_or_sale"]
                        else "temporary" if customs and customs.content_type == "sample"
                        else "return" if customs and customs.content_type in ["return_merchandise", "return_for_repair"]
                        else "permanent"
                    ),
                    manufacturerCountry=item.origin_country or shipper.country_code,
                    weight=mydhl_req.WeightType(
                        netValue=item.weight,
                        grossValue=item.weight,
                    ),
                )
                for index, item in enumerate(commodities_to_use, start=1)
            ]
        else:
            # Create default commodity from package data
            total_weight = sum(p.weight.value for p in packages)
            line_items = [
                mydhl_req.LineItemType(
                    number=1,
                    description=lib.text(
                        packages.description or "Goods",
                        max=75
                    ),
                    price=int(declared_value or 1),
                    quantity=mydhl_req.QuantityType(
                        value=len(packages),
                        unitOfMeasurement="PCS",
                    ),
                    exportReasonType="permanent",
                    manufacturerCountry=shipper.country_code,
                    weight=mydhl_req.WeightType(
                        netValue=total_weight,
                        grossValue=total_weight,
                    ),
                )
            ]

        export_declaration = mydhl_req.ExportDeclarationType(
            lineItems=line_items,
            invoice=mydhl_req.InvoiceType(
                number=(customs.invoice if customs else None) or "INV-00000",
                date=(customs.invoice_date if customs else None) or time.strftime("%Y-%m-%d"),
            ),
        )

    # Build customer details with proper DHL structure
    # DHL requires phone and companyName even for private addresses
    customer_details = mydhl_req.CustomerDetailsType(
        shipperDetails=mydhl_req.ErDetailsType(
            postalAddress=mydhl_req.PostalAddressType(
                postalCode=shipper.postal_code,
                cityName=shipper.city,
                countryCode=shipper.country_code,
                addressLine1=shipper.address_line1,
            ),
            contactInformation=mydhl_req.ContactInformationType(
                email=shipper.email,
                phone=shipper.phone_number or "0000000000",
                companyName=shipper.company_name or shipper.person_name or "N/A",
                fullName=shipper.person_name,
            ),
            typeCode="business" if shipper.company_name else "private",
        ),
        receiverDetails=mydhl_req.ErDetailsType(
            postalAddress=mydhl_req.PostalAddressType(
                postalCode=recipient.postal_code,
                cityName=recipient.city,
                countryCode=recipient.country_code,
                addressLine1=recipient.address_line1,
            ),
            contactInformation=mydhl_req.ContactInformationType(
                email=recipient.email,
                phone=recipient.phone_number or "0000000000",
                companyName=recipient.company_name or recipient.person_name or "N/A",
                fullName=recipient.person_name,
            ),
            typeCode="business" if recipient.company_name else "private",
        ),
    )

    # Build content with packages
    content = mydhl_req.ContentType(
        packages=[
            mydhl_req.PackageType(
                typeCode=provider_units.PackagingType[package.packaging_type or 'your_packaging'].value,
                weight=package.weight.value,
                dimensions=mydhl_req.DimensionsType(
                    length=int(package.length.value) if package.length else None,
                    width=int(package.width.value) if package.width else None,
                    height=int(package.height.value) if package.height else None,
                ) if package.length and package.width and package.height else None,
            )
            for package in packages
        ],
        isCustomsDeclarable=is_international,
        declaredValue=declared_value,
        declaredValueCurrency=declared_currency,
        description=packages.description or "Shipment",
        incoterm=customs.incoterm or "DAP" if (is_international and customs) else None,
        exportDeclaration=export_declaration,
        unitOfMeasurement="metric" if packages.weight_unit == "KG" else "imperial",
    )

    # Build output image properties for label
    output_image_properties = mydhl_req.OutputImagePropertiesType(
        printerDPI=300,
        encodingFormat="pdf" if (payload.label_type or "PDF").lower() == "pdf" else "zpl",
        imageOptions=[
            mydhl_req.ImageOptionType(
                typeCode="label",
                templateName="ECOM26_84_001",
                isRequested=True,
            )
        ],
    )

    # Get planned shipping date
    import datetime
    shipping_date = lib.to_date(payload.options.get("shipment_date") or payload.options.get("shipping_date"))
    if not shipping_date:
        shipping_date = datetime.datetime.now() + datetime.timedelta(days=1)
    planned_date = shipping_date.strftime("%Y-%m-%dT%H:%M:%S GMT+00:00")

    # Create the MyDHL shipment request object
    request = mydhl_req.ShipmentRequestType(
        plannedShippingDateAndTime=planned_date,
        pickup=mydhl_req.PickupType(isRequested=False),
        productCode=service_code,
        localProductCode=service_code,
        getRateEstimates=False,
        accounts=[
            mydhl_req.AccountType(
                typeCode="shipper",
                number=settings.account_number,
            )
        ] if settings.account_number else None,
        outputImageProperties=output_image_properties,
        customerDetails=customer_details,
        content=content,
    )

    return lib.Serializable(request, lib.to_dict)
