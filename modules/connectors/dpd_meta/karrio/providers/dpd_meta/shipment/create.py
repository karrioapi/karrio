"""Karrio DPD META shipment API implementation."""

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dpd_meta.error as error
import karrio.providers.dpd_meta.utils as provider_utils
import karrio.providers.dpd_meta.units as provider_units
import karrio.schemas.dpd_meta.shipment_request as dpd_req
import karrio.schemas.dpd_meta.shipment_response as dpd_res


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    ctx = _response.ctx

    has_shipment = "shipmentId" in response if isinstance(response, dict) else False

    shipment = (
        _extract_details(response, settings, ctx)
        if has_shipment and not any(messages)
        else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict = None,
) -> models.ShipmentDetails:
    """Extract shipment details from DPD META-API response."""
    # fmt: off
    shipment = lib.to_object(dpd_res.ShipmentResponseType, data)
    label_format = (ctx or {}).get("label_format", "PDF")

    [tracking_number, *_] = shipment.parcelIds
    label_data = lib.failsafe(lambda: shipment.label.base64Data)
    documents = [
        ("qr_code", lib.failsafe(lambda: shipment.qrcode.base64Data))
    ]

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=shipment.shipmentId,
        label_type=label_format,
        docs=models.Documents(
            label=label_data,
            extra_documents=[
                models.ShippingDocument(
                    category=provider_units.ShippingDocumentCategory.map(category).name_or_key,
                    base64=document,
                    format="PDF",
                )
                for category, document in documents if document
            ],
        ),
        meta=dict(
            tracking_url=settings.tracking_url.format(tracking_number),
            parcel_barcodes=lib.to_dict(shipment.parcelBarcodes or []),
            network_shipment_id=shipment.networkShipmentId,
            network_parcel_ids=shipment.networkParcelIds,
            tracking_numbers=shipment.parcelIds,
        ),
    )
    # fmt: on


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a DPD META-API shipment request."""
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service).value_or_key
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
    )
    exporter = lib.to_address(
        getattr(payload.customs, "duty_billing_address", None)
        or {
            "sender": payload.shipper,
            "recipient": payload.recipient,
            "third_party": payload.billing_address,
        }.get(customs.duty.paid_by)
        or payload.shipper
    )

    is_international = shipper.country_code != recipient.country_code
    has_customs = customs.is_defined
    currency = options.currency.state or "EUR"
    customs_value = lib.identity(
        customs.duty.declared_value
        if has_customs and customs.duty.declared_value
        else (customs.commodities.value_amount if has_customs else 0)
    )

    label_format = lib.identity(
        settings.connection_config.label_format.state
        or payload.label_type
        or "PDF"
    )
    label_paper_format = lib.identity(
        settings.connection_config.label_paper_format.state
        or options.label_paper_format.state
    )
    label_printer_position = lib.identity(
        settings.connection_config.label_printer_position.state
        or options.label_printer_position.state
    )
    dropoff_type = lib.identity(
        settings.connection_config.dropoff_type.state
        or options.dropoff_type.state
    )
    simulate = lib.identity(
        settings.connection_config.simulate.state
        or options.simulate.state
    )
    extra_barcode = lib.identity(
        settings.connection_config.extra_barcode.state
        or options.extra_barcode.state
    )
    with_document = lib.identity(
        settings.connection_config.with_document.state
        or options.with_document.state
    )

    request = dpd_req.ShipmentRequestElementType(
        numberOfParcels=str(len(packages)),
        shipmentInfos=dpd_req.ShipmentInfosType(
            productCode=service,
            shipmentId=payload.reference,
            weight=str(int(packages.weight.G)),
            cifcost=lib.identity(
                dpd_req.CustomsAmountType(
                    amount=lib.to_money(customs.duty.declared_value),
                    currency=customs.duty.currency or currency,
                )
                if has_customs and customs.duty.declared_value
                else None
            ),
            dimensions=lib.identity(
                dpd_req.DimensionsType(
                    length=int(packages[0].length.CM),
                    width=int(packages[0].width.CM),
                    height=int(packages[0].height.CM),
                )
                if packages[0].has_dimensions
                else None
            ),
        ),
        sender=dpd_req.SenderType(
            customerInfos=dpd_req.CustomerInfosType(
                customerID=settings.customer_id,
                customerAccountNumber=(
                    settings.customer_account_number or settings.customer_id
                ),
            ),
            address=dpd_req.ReceiverAddressType(
                companyName=shipper.company_name or "",
                name1=shipper.person_name or "",
                name2=shipper.address_line2,
                street=shipper.street_name or shipper.address_line1 or "",
                houseNumber=shipper.street_number or "",
                addressLine2=shipper.address_line2,
                floor=shipper.floor,
                building=shipper.building,
                department=shipper.department,
                zipCode=shipper.postal_code,
                city=shipper.city,
                state=shipper.state_code,
                country=shipper.country_code,
            ),
            contact=dpd_req.ReceiverContactType(
                phone1=shipper.phone_number or "",
                email=shipper.email or "",
            ),
            legalEntity=lib.identity(
                dpd_req.LegalEntityType(
                    businessType=provider_units.BusinessType.BUSINESS.value,
                    vatNumber=shipper.tax_id,
                    eori=(
                        customs.options.shipper_eori.state
                        if has_customs and "shipper_eori" in customs.options
                        else None
                    ),
                )
                if shipper.tax_id or (has_customs and "shipper_eori" in customs.options)
                else None
            ),
        ),
        receiver=dpd_req.ReceiverType(
            address=dpd_req.ReceiverAddressType(
                name1=recipient.person_name or "",
                name2=recipient.address_line2,
                companyName=recipient.company_name or "",
                street=recipient.street_name or recipient.address_line1 or "",
                houseNumber=recipient.street_number or "",
                addressLine2=recipient.address_line2,
                floor=recipient.floor,
                building=recipient.building,
                department=recipient.department,
                zipCode=recipient.postal_code,
                city=recipient.city,
                state=recipient.state_code,
                country=recipient.country_code,
            ),
            contact=dpd_req.ReceiverContactType(
                phone1=recipient.phone_number or "",
                email=recipient.email or "",
            ),
            legalEntity=lib.identity(
                dpd_req.LegalEntityType(
                    businessType=lib.identity(
                        provider_units.BusinessType.BUSINESS.value
                        if recipient.company_name
                        else provider_units.BusinessType.PRIVATE.value
                    ),
                    vatNumber=recipient.tax_id,
                    eori=(
                        customs.options.recipient_eori.state
                        if has_customs and "recipient_eori" in customs.options
                        else None
                    ),
                )
                if recipient.tax_id
                or (has_customs and "recipient_eori" in customs.options)
                else None
            ),
        ),
        parcel=[
            dpd_req.ParcelType(
                parcelInfos=dpd_req.ParcelInfosType(
                    weight=str(int(pkg.weight.G)),
                    dimensions=lib.identity(
                        dpd_req.DimensionsType(
                            length=int(pkg.length.CM),
                            width=int(pkg.width.CM),
                            height=int(pkg.height.CM),
                        )
                        if pkg.has_dimensions
                        else None
                    ),
                ),
                parcelContent=pkg.description,
                references=lib.identity(
                    [
                        dpd_req.ReferenceType(
                            referenceNumber=pkg.reference_number,
                            referenceType="CUSTOMER_REFERENCE",
                        )
                    ]
                    if pkg.reference_number
                    else []
                ),
                cod=lib.identity(
                    dpd_req.CodType(
                        amount=dpd_req.CustomsAmountType(
                            amount=lib.to_money(options.cash_on_delivery.state),
                            currency=currency,
                        ),
                        collectType=lib.identity(
                            options.dpd_meta_cod_collect_type.state
                            or provider_units.CodCollectType.CASH.value
                        ),
                        purpose=options.dpd_meta_cod_purpose.state,
                        bankCode=options.dpd_meta_cod_bank_code.state,
                        bankName=options.dpd_meta_cod_bank_name.state,
                        bankAccountNumber=options.dpd_meta_cod_bank_account_number.state,
                        bankAccountName=options.dpd_meta_cod_bank_account_name.state,
                        iban=options.dpd_meta_cod_iban.state,
                        bic=options.dpd_meta_cod_bic.state,
                    )
                    if options.cash_on_delivery.state
                    else None
                ),
                insurance=lib.identity(
                    dpd_req.InsuranceType(
                        insuranceAmount=dpd_req.CustomsAmountType(
                            amount=lib.to_money(options.insurance.state),
                            currency=currency,
                        ),
                        insuranceParcelContent=pkg.description,
                    )
                    if options.insurance.state
                    else None
                ),
                messages=lib.identity(
                    dpd_req.MessagesType(
                        email1=lib.identity(
                            dpd_req.Email1Type(
                                notificationType="DELIVERY",
                                notificationEmail=options.dpd_meta_notification_email.state,
                                notificationLanguage="EN",
                            )
                            if options.dpd_meta_notification_email.state
                            else None
                        ),
                        sms1=lib.identity(
                            dpd_req.Sms1Type(
                                notificationType="DELIVERY",
                                notificationPhone=options.dpd_meta_notification_sms.state,
                                notificationLanguage="EN",
                            )
                            if options.dpd_meta_notification_sms.state
                            else None
                        ),
                    )
                    if (
                        options.dpd_meta_notification_email.state
                        or options.dpd_meta_notification_sms.state
                    )
                    else None
                ),
            )
            for pkg in packages
        ],
        international=lib.identity(
            dpd_req.InternationalType(
                parcelType=lib.identity(
                    provider_units.ParcelType.DOCUMENT.value
                    if customs.content_type == "documents"
                    else provider_units.ParcelType.NON_DOC.value
                ),
                customsAmount=dpd_req.CustomsAmountType(
                    amount=lib.to_money(customs_value),
                    currency=customs.duty.currency or currency,
                ),
                customsAmountEx=dpd_req.CustomsAmountType(
                    amount=lib.to_money(customs_value),
                    currency=customs.duty.currency or currency,
                ),
                customsTerms=lib.identity(
                    provider_units.Incoterm.map(customs.incoterm).value
                    or provider_units.CustomsTerms.DAP_NOT_CLEARED.value
                ),
                customsPaper=provider_units.CustomsPaper.COMMERCIAL_INVOICE.value,
                clearanceStatus=provider_units.ClearanceStatus.NO.value,
                customsHighLowValue=lib.identity(
                    provider_units.CustomsValueLevel.HIGH.value
                    if customs_value >= 150
                    else (
                        provider_units.CustomsValueLevel.MEDIUM.value
                        if customs_value >= 22
                        else provider_units.CustomsValueLevel.LOW.value
                    )
                ),
                customsInvoice=customs.invoice,
                customsInvoiceDates=lib.identity(
                    [customs.invoice_date] if customs.invoice_date else None
                ),
                numberOfArticles=str(len(customs.commodities)),
                exportReason=lib.identity(
                    provider_units.CustomsContentType.map(customs.content_type).value
                    if customs.content_type
                    else provider_units.ExportReason.SALE.value
                ),
                shipmentContent=lib.text(customs.content_description, max=100),
                importer=dpd_req.ImporterType(
                    address=dpd_req.ExporterAddressType(
                        companyName=recipient.company_name,
                        name1=recipient.person_name,
                        street=recipient.street_name or recipient.address_line1,
                        houseNumber=recipient.street_number,
                        zipCode=recipient.postal_code,
                        city=recipient.city,
                        country=recipient.country_code,
                    ),
                    contact=dpd_req.ExporterContactType(
                        phone1=recipient.phone_number,
                        email=recipient.email,
                    ),
                    vatNumber=recipient.tax_id,
                    eori=(
                        customs.options.recipient_eori.state
                        if "recipient_eori" in customs.options
                        else None
                    ),
                ),
                exporter=dpd_req.ExporterType(
                    address=dpd_req.ExporterAddressType(
                        companyName=exporter.company_name,
                        name1=exporter.person_name,
                        street=exporter.address_line1,
                        houseNumber=exporter.street_number,
                        zipCode=exporter.postal_code,
                        city=exporter.city,
                        country=exporter.country_code,
                    ),
                    contact=dpd_req.ExporterContactType(
                        phone1=exporter.phone_number,
                        email=exporter.email,
                    ),
                    eori=customs.options.eori.state,
                ),
                interInvoiceLines=[
                    dpd_req.InterInvoiceLineType(
                        invoicePosition=str(idx + 1),
                        quantityOfItems=str(item.quantity or 1),
                        content=lib.text(item.description, max=35),
                        amountOfPosition=item.value_amount,
                        manufacturedCountry=item.origin_country or shipper.country_code,
                        netWeight=lib.text(item.weight.G),
                        grossWeight=lib.text(item.weight.G),
                        customerProductCode=item.sku,
                        productDescription=lib.text(item.description, max=100),
                        importTarifCode=item.hs_code,
                        exportTarifCode=item.hs_code,
                        parcelRank="1",
                    )
                    for idx, item in enumerate(customs.commodities)
                ],
            )
            if is_international and has_customs
            else None
        ),
        delivery=lib.identity(
            dpd_req.DeliveryType(
                dateFrom=options.dpd_meta_delivery_date_from.state,
                dateTo=options.dpd_meta_delivery_date_to.state,
                timeFrom=options.dpd_meta_delivery_time_from.state,
                timeTo=options.dpd_meta_delivery_time_to.state,
            )
            if any([
                options.dpd_meta_delivery_date_from.state, 
                options.dpd_meta_delivery_date_to.state,
                options.dpd_meta_delivery_time_from.state,
                options.dpd_meta_delivery_time_to.state,
            ])
            else None
        ),
    )

    return lib.Serializable(
        [request],
        lib.to_dict,
        dict(
            label_format=label_format,
            label_paper_format=label_paper_format,
            label_printer_position=label_printer_position,
            dropoff_type=dropoff_type,
            simulate=simulate,
            extra_barcode=extra_barcode,
            with_document=with_document,
        ),
    )
