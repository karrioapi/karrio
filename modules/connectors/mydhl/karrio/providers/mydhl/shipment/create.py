"""Karrio MyDHL shipment API implementation."""

import karrio.schemas.mydhl.shipment_request as mydhl_req
import karrio.schemas.mydhl.shipment_response as mydhl_res

import datetime
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
    paperless_response = _response.ctx.get("paperless_response") or {}

    messages = [
        *error.parse_error_response(response, settings),
        *error.parse_error_response(paperless_response, settings),
    ]

    details = lib.identity(
        _extract_details(
            lib.to_object(mydhl_res.ShipmentResponseType, response),
            settings,
        )
        if response.get("status") is None
        and response.get("shipmentTrackingNumber") is not None
        else None
    )

    return details, messages


def _extract_details(
    shipment: mydhl_res.ShipmentResponseType,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    tracking_number = str(shipment.shipmentTrackingNumber or "")
    label_doc = next(
        (doc for doc in (shipment.documents or []) if doc and doc.content),
        None,
    )
    label = label_doc.content if label_doc else ""
    label_format = label_doc.imageFormat if label_doc else "PDF"
    package_tracking_numbers = [
        pkg.trackingNumber
        for pkg in (shipment.packages or [])
        if pkg and pkg.trackingNumber
    ]
    shipment_charge = next(iter(shipment.shipmentCharges or []), None)

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=tracking_number,
        label_type=label_format,
        docs=models.Documents(label=label),
        selected_rate=lib.identity(
            models.RateDetails(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                service=settings.carrier_name,
                total_charge=lib.to_money(shipment_charge.price),
                currency=shipment_charge.priceCurrency,
                extra_charges=[
                    models.ChargeDetails(
                        name=charge.name,
                        amount=lib.to_money(charge.price),
                        currency=shipment_charge.priceCurrency,
                    )
                    for charge in (shipment_charge.serviceBreakdown or [])
                    if charge.name and charge.price
                ],
            )
            if shipment_charge and shipment_charge.price
            else None
        ),
        meta=dict(
            tracking_url=shipment.trackingUrl or "",
            package_tracking_numbers=package_tracking_numbers or None,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a shipment request for MyDHL API."""

    # === Input transformation phase ===
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    is_international = shipper.country_code != recipient.country_code
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
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
                            sku="0000",
                            quantity=1,
                            weight=packages.weight.value,
                            weight_unit=packages.weight_unit,
                            description=packages.description or "Goods",
                        )
                    ]
                )
            )
            if is_international
            else None
        ),
    )

    # === Pre-computation phase ===
    service_code = provider_units.ShippingService.map(payload.service).value_or_key
    weight_unit = "metric" if packages.weight_unit == "KG" else "imperial"
    label_format = provider_units.LabelFormat.map(
        payload.label_type or "PDF"
    ).value_or_key.lower()
    currency = options.currency.state or customs.duty.currency or "USD"
    declared_value = (
        lib.identity(
            options.declared_value.state
            or customs.duty.declared_value
            or customs.commodities.value_amount
            or packages.total_value
            or 1.0
        )
        if is_international
        else None
    )

    # Export reason mapping
    export_reason = lib.identity(
        "permanent"
        if customs.content_type in ["merchandise", "commercial_purpose_or_sale"]
        else (
            "temporary"
            if customs.content_type == "sample"
            else (
                "return"
                if customs.content_type in ["return_merchandise", "return_for_repair"]
                else "permanent"
            )
        )
    )

    # Invoice details
    invoice_number = customs.invoice or "INV-00000"
    invoice_date = lib.fdate(customs.invoice_date) or lib.fdate(datetime.datetime.now())

    # Incoterm and planned shipping date
    planned_date = lib.fdatetime(
        options.shipment_date.state or datetime.datetime.now(),
        "%Y-%m-%dT%H:%M:%S GMT+00:00",
    )
    planned_ship_date = lib.fdate(
        options.shipment_date.state or datetime.datetime.now()
    )

    # Paperless trade documents - extract commercial invoice from doc_files
    doc_files = options.doc_files.state or []
    paperless_documents = [
        doc
        for doc in doc_files
        if doc.get("doc_type")
        in ["commercial_invoice", "invoice", "proforma", "certificate_of_origin"]
        and doc.get("doc_file")
    ]
    is_paperless = is_international and any(paperless_documents)

    # === Request tree building phase ===
    request = mydhl_req.ShipmentRequestType(
        plannedShippingDateAndTime=planned_date,
        pickup=mydhl_req.PickupType(isRequested=False),
        productCode=service_code,
        localProductCode=service_code,
        getRateEstimates=True,
        accounts=[
            mydhl_req.AccountType(typeCode="shipper", number=settings.account_number)
        ],
        outputImageProperties=mydhl_req.OutputImagePropertiesType(
            printerDPI=300,
            encodingFormat=label_format,
            imageOptions=[
                mydhl_req.ImageOptionType(
                    typeCode="label",
                    templateName="ECOM26_84_001",
                    isRequested=True,
                )
            ],
        ),
        customerDetails=mydhl_req.CustomerDetailsType(
            shipperDetails=mydhl_req.DetailsType(
                postalAddress=mydhl_req.PostalAddressType(
                    postalCode=shipper.postal_code,
                    cityName=shipper.city,
                    countryCode=shipper.country_code,
                    provinceCode=shipper.state_code,
                    addressLine1=shipper.address_line1,
                    addressLine2=shipper.address_line2,
                    addressLine3=shipper.extra,
                    countyName=shipper.suburb,
                    provinceName=shipper.state_name,
                    countryName=shipper.country_name,
                ),
                contactInformation=mydhl_req.ContactInformationType(
                    email=shipper.email,
                    phone=shipper.phone_number or "0000000000",
                    mobilePhone=shipper.phone_number,
                    companyName=shipper.company_name or shipper.person_name or "N/A",
                    fullName=shipper.person_name,
                ),
                typeCode="business" if shipper.company_name else "private",
            ),
            receiverDetails=mydhl_req.DetailsType(
                postalAddress=mydhl_req.PostalAddressType(
                    postalCode=recipient.postal_code,
                    cityName=recipient.city,
                    countryCode=recipient.country_code,
                    provinceCode=recipient.state_code,
                    addressLine1=recipient.address_line1,
                    addressLine2=recipient.address_line2,
                    addressLine3=recipient.extra,
                    countyName=recipient.suburb,
                    provinceName=recipient.state_name,
                    countryName=recipient.country_name,
                ),
                contactInformation=mydhl_req.ContactInformationType(
                    email=recipient.email,
                    phone=recipient.phone_number or "0000000000",
                    mobilePhone=recipient.phone_number,
                    companyName=recipient.company_name
                    or recipient.person_name
                    or "N/A",
                    fullName=recipient.person_name,
                ),
                typeCode="business" if recipient.company_name else "private",
            ),
        ),
        content=mydhl_req.ContentType(
            packages=[
                mydhl_req.PackageType(
                    typeCode=provider_units.PackagingType.map(
                        package.packaging_type or "your_packaging"
                    ).value,
                    weight=package.weight.value,
                    dimensions=lib.identity(
                        mydhl_req.DimensionsType(
                            length=int(package.length.value),
                            width=int(package.width.value),
                            height=int(package.height.value),
                        )
                        if package.length.value
                        and package.width.value
                        and package.height.value
                        else None
                    ),
                )
                for package in packages
            ],
            isCustomsDeclarable=is_international,
            declaredValue=declared_value,
            declaredValueCurrency=currency if is_international else None,
            description=packages.description or "Shipment",
            incoterm=lib.identity(
                customs.incoterm or "DDU" if is_international else None
            ),
            exportDeclaration=lib.identity(
                mydhl_req.ExportDeclarationType(
                    lineItems=[
                        mydhl_req.LineItemType(
                            number=index,
                            description=lib.text(
                                item.description or item.title or "Commodity", max=75
                            ),
                            price=int(item.value_amount or 0),
                            quantity=mydhl_req.QuantityType(
                                value=item.quantity,
                                unitOfMeasurement="PCS",
                            ),
                            commodityCodes=(
                                [
                                    mydhl_req.SpecialInstructionType(
                                        typeCode="outbound", value=item.hs_code
                                    )
                                ]
                                if item.hs_code
                                else []
                            ),
                            exportReasonType=export_reason,
                            manufacturerCountry=item.origin_country
                            or shipper.country_code,
                            weight=mydhl_req.WeightType(
                                netValue=item.weight, grossValue=item.weight
                            ),
                        )
                        for index, item in enumerate(customs.commodities, start=1)
                    ],
                    invoice=mydhl_req.InvoiceType(
                        number=invoice_number, date=invoice_date
                    ),
                )
                if is_international
                else None
            ),
            unitOfMeasurement=weight_unit,
        ),
    )

    # Build paperless trade request if documents are attached
    paperless_request = lib.identity(
        dict(
            originalPlannedShippingDate=planned_ship_date,
            accounts=[dict(typeCode="shipper", number=settings.account_number)],
            productCode=service_code,
            documentImages=[
                dict(
                    typeCode=lib.identity(
                        "CIN"
                        if doc.get("doc_type") == "commercial_invoice"
                        else (
                            "INV"
                            if doc.get("doc_type") == "invoice"
                            else (
                                "PNV"
                                if doc.get("doc_type") == "proforma"
                                else (
                                    "COO"
                                    if doc.get("doc_type") == "certificate_of_origin"
                                    else "CIN"
                                )
                            )
                        )
                    ),
                    imageFormat=(doc.get("doc_format") or "PDF").upper(),
                    content=doc.get("doc_file"),
                )
                for doc in paperless_documents
            ],
        )
        if is_paperless
        else None
    )

    return lib.Serializable(
        dict(shipment=request, paperless=paperless_request),
        lambda req: dict(
            shipment=lib.to_dict(req["shipment"]),
            paperless=lib.to_dict(req["paperless"]) if req.get("paperless") else None,
        ),
        dict(is_paperless=is_paperless),
    )
