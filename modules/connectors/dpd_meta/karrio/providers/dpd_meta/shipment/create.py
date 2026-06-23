"""Karrio DPD META shipment API implementation."""

import math

import karrio.core.models as models
import karrio.core.units as units
import karrio.lib as lib
import karrio.providers.dpd_meta.error as error
import karrio.providers.dpd_meta.location as provider_location
import karrio.providers.dpd_meta.units as provider_units
import karrio.providers.dpd_meta.utils as provider_utils
import karrio.schemas.dpd_meta.shipment_request as dpd_req
import karrio.schemas.dpd_meta.shipment_response as dpd_res


def _round_grams(g: float) -> int:
    # DPD META divides weight by 10 before passing to SOAP BU-API (10 g units)
    return math.ceil(g / 10) * 10


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> tuple[models.ShipmentDetails, list[models.Message]]:
    response = _response.deserialize()
    ctx = _response.ctx
    messages = error.parse_error_response(response, settings)

    shipment_data = response[0] if isinstance(response, list) else response

    has_shipment = isinstance(shipment_data, dict) and "shipmentId" in shipment_data

    shipment = _extract_details(shipment_data, settings, ctx) if has_shipment and not any(messages) else None

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
    # Intra-EU cross-border shipments don't require customs data per DPD spec.
    is_eu_internal = (
        shipper.country_code in provider_units.EU_MEMBER_STATES
        and recipient.country_code in provider_units.EU_MEMBER_STATES
    )
    has_customs = (
        customs.is_defined
        and is_international
        and (not is_eu_internal or service == provider_units.ShippingService.dpd_meta_international_express.value)
    )
    currency = options.currency.state or "EUR"
    customs_value = lib.identity(
        customs.duty.declared_value
        if has_customs and customs.duty.declared_value
        else (customs.commodities.value_amount if has_customs else 0)
    )

    label_format = lib.identity(settings.connection_config.label_format.state or payload.label_type or "PDF")
    label_paper_format = lib.identity(
        settings.connection_config.label_paper_format.state or options.label_paper_format.state
    )
    label_printer_position = lib.identity(
        settings.connection_config.label_printer_position.state or options.label_printer_position.state
    )
    dropoff_type = lib.identity(settings.connection_config.dropoff_type.state or options.dropoff_type.state)
    simulate = lib.identity(settings.connection_config.simulate.state or options.simulate.state)
    extra_barcode = lib.identity(settings.connection_config.extra_barcode.state or options.extra_barcode.state)
    with_document = lib.identity(settings.connection_config.with_document.state or options.with_document.state)
    product_code = provider_units.resolve_product_code(service, options, recipient.country_code)
    pudo_id = provider_units.resolve_pudo_id(options, product_code)
    # A connection may pin the depot via `sending_depot` config; otherwise it is
    # resolved per shipment from the sender postal code via the DepotDataService.
    depot_override = provider_utils.configured_depot(settings, geo_routing=True)
    resolve_depot = depot_override is None and provider_units.should_resolve_shipper_depot(
        options, shipper.country_code
    )
    depot_query = (
        provider_location.location_request(models.LocationRequest(address=payload.shipper), settings)
        if resolve_depot
        else None
    )
    notification_email = options.dpd_meta_notification_email.state or (
        recipient.email
        if (pudo_id or (product_code in provider_units.B2C_PRODUCT_CODES and product_code != "332"))
        else None
    )

    request = dpd_req.ShipmentRequestElementType(
        customerReferenceNumbers=([lib.text(payload.reference, max=35)] if payload.reference else None),
        numberOfParcels=str(len(packages)),
        sendingDepot=depot_override or (provider_units.DEPOT_PLACEHOLDER if resolve_depot else None),
        shipmentInfos=dpd_req.ShipmentInfosType(
            productCode=product_code,
            additionalServiceCode=provider_units.ADDITIONAL_SERVICE_CODES.get(product_code),
            weight=str(sum(_round_grams(pkg.weight.G) for pkg in packages)),
            cifcost=lib.identity(
                dpd_req.CustomsAmountType(
                    amount=lib.to_money(customs.duty.declared_value),
                    currency=customs.duty.currency or currency,
                )
                if has_customs and customs.duty.declared_value
                else None
            ),
        ),
        sender=dpd_req.SenderType(
            address=dpd_req.ReceiverAddressType(
                companyName=lib.text(shipper.company_name or "", max=35),
                name1=lib.text(shipper.company_name or shipper.person_name or "", max=35),
                name2=lib.text(shipper.person_name if shipper.company_name else "", max=35),
                street=lib.text(shipper.street_name or shipper.address_line1 or "", max=35),
                houseNumber=lib.text(shipper.street_number or "", max=8),
                addressLine2=lib.text(shipper.address_line2, max=35),
                floor=lib.text(shipper.floor, max=35),
                building=lib.text(shipper.building, max=35),
                department=lib.text(shipper.department, max=35),
                zipCode=lib.text(shipper.postal_code, max=9),
                city=lib.text(shipper.city, max=35),
                state=lib.text(shipper.state_code, max=2),
                country=shipper.country_code,
            ),
            contact=dpd_req.ReceiverContactType(
                phone1=lib.identity(lib.text(shipper.phone_number, max=30) or ""),
                email=shipper.email or "",
            ),
            legalEntity=lib.identity(
                dpd_req.LegalEntityType(
                    businessType=provider_units.BusinessType.BUSINESS.value,
                    vatNumber=lib.text(shipper.tax_id, max=20),
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
            pudoId=pudo_id,
            address=dpd_req.ReceiverAddressType(
                name1=lib.text(recipient.company_name or recipient.person_name or "", max=35),
                name2=lib.text(recipient.person_name if recipient.company_name else "", max=35),
                companyName=lib.text(recipient.company_name or "", max=35),
                street=lib.text(recipient.street_name or recipient.address_line1 or "", max=35),
                houseNumber=lib.text(recipient.street_number or "", max=8),
                addressLine2=lib.text(recipient.address_line2, max=35),
                floor=lib.text(recipient.floor, max=35),
                building=lib.text(recipient.building, max=35),
                department=lib.text(recipient.department, max=35),
                zipCode=lib.text(recipient.postal_code, max=9),
                city=lib.text(recipient.city, max=35),
                state=lib.text(recipient.state_code, max=2),
                country=recipient.country_code,
            ),
            contact=dpd_req.ReceiverContactType(
                phone1=lib.identity(lib.text(recipient.phone_number, max=30) or ""),
                email=recipient.email or "",
            ),
            legalEntity=lib.identity(
                dpd_req.LegalEntityType(
                    businessType=lib.identity(
                        provider_units.BusinessType.BUSINESS.value
                        if recipient.company_name
                        else provider_units.BusinessType.PRIVATE.value
                    ),
                    vatNumber=lib.text(recipient.tax_id, max=20),
                    eori=(
                        customs.options.recipient_eori.state
                        if has_customs and "recipient_eori" in customs.options
                        else None
                    ),
                )
                if recipient.tax_id or (has_customs and "recipient_eori" in customs.options)
                else None
            ),
        ),
        parcel=[
            dpd_req.ParcelType(
                parcelInfos=dpd_req.ParcelInfosType(
                    weight=str(_round_grams(pkg.weight.G)),
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
                parcelContent=lib.text(pkg.description, max=50),
                senderParcelRefs=lib.identity(
                    [lib.text(pkg.reference_number, max=35)]
                    if pkg.reference_number and pkg.reference_number != (pkg.parcel.id or "").replace("pcl_", "")
                    else None
                ),
                cod=lib.identity(
                    dpd_req.CodType(
                        amount=dpd_req.CustomsAmountType(
                            amount=lib.to_money(options.cash_on_delivery.state),
                            currency=currency,
                        ),
                        collectType=lib.identity(
                            options.dpd_meta_cod_collect_type.state or provider_units.CodCollectType.CASH.value
                        ),
                        purpose=lib.text(
                            options.dpd_meta_cod_purpose.state or settings.connection_config.cod_purpose.state,
                            max=14,
                        ),
                        bankCode=lib.text(
                            options.dpd_meta_cod_bank_code.state or settings.connection_config.cod_bank_code.state,
                            max=25,
                        ),
                        bankName=lib.text(
                            options.dpd_meta_cod_bank_name.state or settings.connection_config.cod_bank_name.state,
                            max=27,
                        ),
                        bankAccountNumber=lib.text(
                            options.dpd_meta_cod_bank_account_number.state
                            or settings.connection_config.cod_bank_account_number.state,
                            max=25,
                        ),
                        bankAccountName=lib.text(
                            options.dpd_meta_cod_bank_account_name.state
                            or settings.connection_config.cod_bank_account_name.state,
                            max=30,
                        ),
                        iban=lib.text(
                            options.dpd_meta_cod_iban.state or settings.connection_config.cod_iban.state,
                            max=50,
                        ),
                        bic=lib.text(
                            options.dpd_meta_cod_bic.state or settings.connection_config.cod_bic.state,
                            max=50,
                        ),
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
                        insuranceParcelContent=lib.text(
                            options.dpd_meta_insurance_description.state or pkg.description,
                            max=35,
                        ),
                    )
                    if options.insurance.state
                    else None
                ),
                hazardous=lib.identity(
                    [
                        dpd_req.HazardousType(
                            classCode=options.dpd_meta_dg_hazard_class.state,
                            identificationClass=options.dpd_meta_dg_identification_class.state,
                            substanceWeight=lib.identity(
                                str(int(round(options.dpd_meta_dg_weight.state * 1000)))
                                if options.dpd_meta_dg_weight.state is not None
                                else None
                            ),
                            factor=options.dpd_meta_dg_hazard_factor.state,
                            notOtherwiseSpecified=options.dpd_meta_dg_nag_entry.state,
                            packingGroup=options.dpd_meta_dg_packing_group.state,
                            subsidiaryRisk=options.dpd_meta_dg_subsidiary_risks.state,
                            description=options.dpd_meta_dg_description.state,
                            tunnelRestrictionCode=options.dpd_meta_dg_tunnel_restriction_code.state,
                            identificationUnNo=options.dpd_meta_dg_un_number.state,
                            packingCode=options.dpd_meta_dg_packing_code.state,
                        )
                    ]
                    if options.dpd_meta_dangerous_goods.state
                    else []
                ),
                messages=[
                    *(
                        [
                            dpd_req.MessageType(
                                messageType="EMAIL",
                                messageDestination=notification_email,
                                messageLanguage="EN",
                            )
                        ]
                        if notification_email
                        else []
                    ),
                    *(
                        [
                            dpd_req.MessageType(
                                messageType="SMS",
                                messageDestination=options.dpd_meta_notification_sms.state,
                                messageLanguage="EN",
                            )
                        ]
                        if options.dpd_meta_notification_sms.state
                        else []
                    ),
                ],
                hazardousLimitedQuantities=lib.identity(
                    True if options.dpd_meta_hazardous_limited_quantities.state else None
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
                customsInvoice=lib.text(customs.invoice or payload.reference or "N/A", max=35),
                customsInvoiceDates=lib.identity([customs.invoice_date] if customs.invoice_date else None),
                numberOfArticles=str(len(customs.commodities)),
                exportReason=lib.identity(
                    provider_units.CustomsContentType.map(customs.content_type).value
                    if customs.content_type
                    else provider_units.ExportReason.SALE.value
                ),
                shipmentContent=lib.text(customs.content_description, max=100),
                importer=dpd_req.ImporterType(
                    address=dpd_req.ExporterAddressType(
                        name1=lib.text(recipient.company_name or recipient.person_name, max=35),
                        street=lib.text(recipient.street_name or recipient.address_line1, max=35),
                        houseNumber=lib.text(recipient.street_number, max=8),
                        zipCode=lib.text(recipient.postal_code, max=9),
                        city=lib.text(recipient.city, max=35),
                        country=recipient.country_code,
                    ),
                    contact=dpd_req.ExporterContactType(
                        contactPerson=lib.text(recipient.person_name, max=35),
                        phone1=lib.identity(lib.text(recipient.phone_number, max=30) or None),
                        email=recipient.email,
                    ),
                    vatNumber=lib.text(recipient.tax_id, max=20),
                    eori=(customs.options.recipient_eori.state if "recipient_eori" in customs.options else None),
                ),
                exporter=dpd_req.ExporterType(
                    address=dpd_req.ExporterAddressType(
                        name1=lib.text(exporter.company_name or exporter.person_name, max=35),
                        street=lib.text(exporter.address_line1, max=35),
                        houseNumber=lib.text(exporter.street_number, max=8),
                        zipCode=lib.text(exporter.postal_code, max=9),
                        city=lib.text(exporter.city, max=35),
                        country=exporter.country_code,
                    ),
                    contact=dpd_req.ExporterContactType(
                        contactPerson=lib.text(exporter.person_name, max=35),
                        phone1=lib.identity(lib.text(exporter.phone_number, max=30) or None),
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
                        netWeight=str(lib.to_int(units.Weight(item.weight, item.weight_unit or "KG").G)),
                        grossWeight=str(lib.to_int(units.Weight(item.weight, item.weight_unit or "KG").G)),
                        customerProductCode=item.sku,
                        productDescription=lib.text(item.description, max=100),
                        importTarifCode=item.hs_code,
                        exportTarifCode=item.hs_code,
                        parcelRank="1",
                    )
                    for idx, item in enumerate(customs.commodities)
                ],
            )
            if has_customs
            else None
        ),
        delivery=lib.identity(
            dpd_req.DeliveryType(
                dateFrom=options.dpd_meta_delivery_date_from.state,
                dateTo=options.dpd_meta_delivery_date_to.state,
                timeFrom=options.dpd_meta_delivery_time_from.state,
                timeTo=options.dpd_meta_delivery_time_to.state,
            )
            if any(
                [
                    options.dpd_meta_delivery_date_from.state,
                    options.dpd_meta_delivery_date_to.state,
                    options.dpd_meta_delivery_time_from.state,
                    options.dpd_meta_delivery_time_to.state,
                ]
            )
            else None
        ),
        person=lib.identity(dpd_req.PersonType(personalDeliveryType="s2") if options.dpd_meta_id_check.state else None),
        mpsCompleteDelivery="s2" if options.cash_on_delivery.state else None,
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
            resolve_depot=resolve_depot,
            depot_query=depot_query,
        ),
    )
