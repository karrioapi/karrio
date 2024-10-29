import karrio.schemas.dhl_express.ship_val_global_req_10_0 as dhl
import karrio.schemas.dhl_express.ship_val_global_res_10_0 as dhl_res
import karrio.schemas.dhl_express.datatypes_global_v10 as dhl_global
import time
import typing
import base64
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.core.errors as errors
import karrio.providers.dhl_express.error as provider_error
import karrio.providers.dhl_express.units as provider_units
import karrio.providers.dhl_express.utils as provider_utils


def parse_shipment_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    air_way_bill = lib.find_element("AirwayBillNumber", response, first=True)

    return (
        _extract_shipment(response, settings) if air_way_bill is not None else None,
        provider_error.parse_error_response(response, settings),
    )


def _extract_shipment(
    shipment_node, settings: provider_utils.Settings
) -> typing.Optional[models.ShipmentDetails]:
    tracking_number = lib.find_element(
        "AirwayBillNumber", shipment_node, first=True
    ).text
    label_image = lib.find_element(
        "LabelImage", shipment_node, dhl_res.LabelImage, first=True
    )
    multilabels: typing.List[dhl_res.MultiLabelType] = lib.find_element(
        "MultiLabel", shipment_node, dhl_res.MultiLabelType
    )
    invoice = next(
        (item for item in multilabels if item.DocName == "CustomInvoiceImage"), None
    )

    label = base64.encodebytes(label_image.OutputImage).decode("utf-8")
    invoice_data = (
        dict(invoice=base64.encodebytes(invoice.DocImageVal).decode("utf-8"))
        if invoice is not None
        else {}
    )

    return models.ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=tracking_number,
        shipment_identifier=tracking_number,
        docs=models.Documents(label=label, **invoice_data),
        meta=dict(
            carrier_tracking_link=settings.tracking_url.format(tracking_number),
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest, settings: provider_utils.Settings
) -> lib.Serializable:
    if any(settings.account_country_code or "") and (
        payload.shipper.country_code != settings.account_country_code
    ):
        raise errors.OriginNotServicedError(payload.shipper.country_code)

    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(
        payload.parcels,
        provider_units.PackagePresets,
        required=["weight"],
        max_weight=units.Weight(300, "KG"),
        package_option_type=provider_units.ShippingOption,
    )
    product = provider_units.ShippingService.map(payload.service).value_or_key

    weight_unit, dim_unit = lib.identity(
        provider_units.COUNTRY_PREFERED_UNITS.get(payload.shipper.country_code)
        or packages.compatible_units
    )
    package_type = provider_units.PackageType.map(packages.package_type).value
    label_format, label_template = provider_units.LabelType[
        payload.label_type or "PDF_6x4"
    ].value
    payment = payload.payment or models.Payment(
        paid_by="sender",
        account_number=settings.account_number,
    )
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit=weight_unit.value,
    )
    is_document = all(p.parcel.is_document for p in packages)
    is_international = shipper.country_code != recipient.country_code
    is_from_EU = payload.shipper.country_code in units.EUCountry
    is_to_EU = payload.recipient.country_code in units.EUCountry
    is_dutiable = is_international and not is_document and not (is_from_EU and is_to_EU)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        origin_country=shipper.country_code,
        initializer=provider_units.shipping_options_initializer,
    )
    option_items = [
        option for _, option in options.items() if option.state is not False
    ]
    duty = customs.duty or models.Duty(paid_by="sender")
    content = lib.identity(
        options.dhl_shipment_content.state
        or customs.content_description
        or packages.content
        or packages.description
        or "N/A"
    )
    reference = payload.reference or getattr(payload, "id", None)
    currency = lib.identity(
        options.currency.state
        or units.CountryCurrency.map(payload.shipper.country_code).value
        or settings.default_currency
    )

    request = dhl.ShipmentRequest(
        schemaVersion="10.0",
        Request=settings.Request(
            MetaData=dhl.MetaData(SoftwareName="3PV", SoftwareVersion="10.0")
        ),
        RegionCode=provider_units.CountryRegion[shipper.country_code].value,
        LanguageCode="en",
        LatinResponseInd=None,
        Billing=dhl.Billing(
            ShipperAccountNumber=settings.account_number,
            ShippingPaymentType=provider_units.PaymentType[payment.paid_by].value,
            BillingAccountNumber=payment.account_number,
            DutyAccountNumber=duty.account_number,
        ),
        Consignee=dhl.Consignee(
            CompanyName=recipient.company_name or "N/A",
            SuiteDepartmentName=None,
            AddressLine1=recipient.street,
            AddressLine2=lib.text(recipient.address_line2),
            AddressLine3=None,
            City=recipient.city,
            Division=None,
            DivisionCode=recipient.state_code,
            PostalCode=recipient.postal_code,
            CountryCode=recipient.country_code,
            CountryName=recipient.country_name,
            Contact=dhl.Contact(
                PersonName=recipient.person_name,
                PhoneNumber=recipient.phone_number or "0000",
                Email=recipient.email,
            ),
            Suburb=None,
            StreetName=recipient.street_name,
            BuildingName=None,
            StreetNumber=recipient.street_number,
            RegistrationNumbers=(
                dhl.RegistrationNumbers(
                    RegistrationNumber=[
                        dhl.RegistrationNumber(
                            Number=recipient.tax_id,
                            NumberTypeCode="VAT",
                            NumberIssuerCountryCode=recipient.country_code,
                        )
                    ]
                )
                if recipient.tax_id is not None
                else None
            ),
            BusinessPartyTypeCode=None,
        ),
        Commodity=lib.identity(
            [
                dhl.Commodity(
                    CommodityCode=c.hs_code or c.sku or "N/A",
                    CommodityName=lib.text(c.title or c.description, max=35),
                )
                for c in customs.commodities
            ]
            if any(customs.commodities)
            else None
        ),
        Dutiable=lib.identity(
            dhl_global.Dutiable(
                DeclaredValue=(
                    duty.declared_value or options.declared_value.state or 1.0
                ),
                DeclaredCurrency=(duty.currency or currency),
                ScheduleB=None,
                ExportLicense=customs.options.license_number.state,
                ShipperEIN=(
                    customs.options.ein.state or customs.duty_billing_address.tax_id
                ),
                ShipperIDType=None,
                TermsOfTrade=customs.incoterm or "DDP",
                CommerceLicensed=None,
                Filing=(
                    dhl_global.Filing(
                        FilingType=dhl_global.FilingType.AES_4.value,
                        FTSR=None,
                        ITN=None,
                        AES4EIN=customs.options.aes.state,
                    )
                    if customs.options.aes.state is not None
                    else None
                ),
            )
            if is_dutiable
            else None
        ),
        UseDHLInvoice=("Y" if is_dutiable else None),
        DHLInvoiceLanguageCode=("en" if is_dutiable else None),
        DHLInvoiceType=lib.identity(
            ("CMI" if customs.commercial_invoice else "PFI") if is_dutiable else None
        ),
        ExportDeclaration=lib.identity(
            dhl_global.ExportDeclaration(
                InterConsignee=None,
                IsPartiesRelation=None,
                ECCN=None,
                SignatureName=customs.signer,
                SignatureTitle=None,
                ExportReason=customs.content_type,
                ExportReasonCode=provider_units.ExportReasonCode[
                    customs.content_type or "other"
                ].value,
                SedNumber=None,
                SedNumberType=None,
                MxStateCode=None,
                InvoiceNumber=(customs.invoice or "0000000"),
                InvoiceDate=(customs.invoice_date or time.strftime("%Y-%m-%d")),
                Remarks=customs.content_description,
                DestinationPort=None,
                TermsOfPayment=None,
                PayerGSTVAT=(
                    customs.options.vat_registration_number.state
                    or customs.duty_billing_address.state_tax_id
                ),
                SignatureImage=None,
                ReceiverReference=None,
                ExporterId=None,
                ExporterCode=None,
                ExportLineItem=[
                    dhl_global.ExportLineItem(
                        LineNumber=index,
                        Quantity=item.quantity,
                        QuantityUnit="PCS",
                        Description=lib.text(
                            item.description or item.title or "N/A", max=75
                        ),
                        Value=item.value_amount or 0.0,
                        IsDomestic=None,
                        CommodityCode=item.hs_code,
                        ScheduleB=None,
                        ECCN=None,
                        Weight=dhl.WeightType(
                            Weight=item.weight,
                            WeightUnit=provider_units.WeightUnit[
                                item.weight_unit
                            ].value,
                        ),
                        GrossWeight=dhl.WeightType(
                            Weight=item.weight,
                            WeightUnit=provider_units.WeightUnit[
                                item.weight_unit
                            ].value,
                        ),
                        License=None,
                        LicenseSymbol=None,
                        ManufactureCountryCode=(
                            item.origin_country or shipper.country_code
                        ),
                        ManufactureCountryName=lib.to_country_name(
                            item.origin_country or shipper.country_code
                        ),
                        ImportTaxManagedOutsideDhlExpress=None,
                        AdditionalInformation=None,
                        ImportCommodityCode=item.hs_code,
                        ItemReferences=None,
                        CustomsPaperworks=None,
                    )
                    for (index, item) in enumerate(customs.commodities, start=1)
                ],
                ShipmentDocument=None,
                InvoiceInstructions=customs.content_description,
                CustomerDataTextEntries=None,
                PlaceOfIncoterm="N/A",
                ShipmentPurpose=(
                    "COMMERCIAL" if customs.commercial_invoice else "PERSONAL"
                ),
                DocumentFunction=None,
                CustomsDocuments=lib.identity(
                    dhl_global.CustomsDocuments(
                        CustomsDocument=[
                            dhl.CustomsDocument(
                                CustomsDocumentID=doc["doc_id"],
                                CustomsDocumentType="IN",
                            )
                            for doc in options.doc_references.state
                        ]
                    )
                    if (
                        options.dhl_paperless_trade.state == True
                        and any(options.doc_references.state or [])
                    )
                    else None
                ),
                InvoiceTotalNetWeight=None,
                InvoiceTotalGrossWeight=None,
                InvoiceReferences=None,
            )
            if is_dutiable
            else None
        ),
        Reference=lib.identity(
            [dhl.Reference(ReferenceID=lib.text(reference, max=30))]
            if any(reference or "")
            else None
        ),
        ShipmentDetails=dhl.ShipmentDetails(
            Pieces=dhl_global.Pieces(
                Piece=[
                    dhl_global.Piece(
                        PieceID=index,
                        PackageType=(
                            package_type
                            or provider_units.PackageType[
                                package.packaging_type or "your_packaging"
                            ].value
                        ),
                        Depth=package.length.map(provider_units.MeasurementOptions)[
                            dim_unit.name
                        ],
                        Width=package.width.map(provider_units.MeasurementOptions)[
                            dim_unit.name
                        ],
                        Height=package.height.map(provider_units.MeasurementOptions)[
                            dim_unit.name
                        ],
                        Weight=package.weight[weight_unit.name],
                        PieceContents=(
                            package.parcel.content or package.parcel.description
                        ),
                        PieceReference=(
                            [
                                dhl.Reference(
                                    ReferenceID=lib.text(package.parcel.id, max=30)
                                )
                            ]
                            if package.parcel.id is not None
                            else None
                        ),
                        AdditionalInformation=(
                            dhl.AdditionalInformation(
                                CustomerDescription=package.parcel.description
                            )
                            if package.parcel.description is not None
                            else None
                        ),
                    )
                    for (index, package) in enumerate(packages, start=1)
                ]
            ),
            WeightUnit=provider_units.WeightUnit[weight_unit.name].value,
            GlobalProductCode=product,
            LocalProductCode=product,
            Date=(options.shipment_date.state or time.strftime("%Y-%m-%d")),
            Contents=content,
            DimensionUnit=provider_units.DimensionUnit[dim_unit.name].value,
            PackageType=package_type,
            IsDutiable=("Y" if is_dutiable else "N"),
            CurrencyCode=currency,
            CustData=getattr(payload, "id", None),
            ShipmentCharges=lib.identity(
                options.cash_on_delivery.state
                if options.cash_on_delivery.state
                else None
            ),
            ParentShipmentIdentificationNumber=None,
            ParentShipmentGlobalProductCode=None,
            ParentShipmentPackagesCount=None,
        ),
        Shipper=dhl.Shipper(
            ShipperID=settings.account_number or "N/A",
            CompanyName=shipper.company_name or "N/A",
            SuiteDepartmentName=None,
            RegisteredAccount=settings.account_number,
            AddressLine1=shipper.street,
            AddressLine2=lib.join(shipper.address_line2, join=True),
            AddressLine3=None,
            City=shipper.city,
            Division=None,
            DivisionCode=shipper.state_code,
            PostalCode=shipper.postal_code,
            OriginServiceAreaCode=None,
            OriginFacilityCode=None,
            CountryCode=shipper.country_code,
            CountryName=shipper.country_name,
            Contact=dhl.Contact(
                PersonName=shipper.person_name,
                PhoneNumber=shipper.phone_number or "0000",
                Email=shipper.email,
            ),
            Suburb=None,
            StreetName=shipper.street_name,
            BuildingName=None,
            StreetNumber=shipper.street_number,
            RegistrationNumbers=(
                dhl.RegistrationNumbers(
                    RegistrationNumber=[
                        dhl.RegistrationNumber(
                            Number=shipper.tax_id,
                            NumberTypeCode="VAT",
                            NumberIssuerCountryCode=shipper.country_code,
                        )
                    ]
                )
                if shipper.tax_id is not None
                else None
            ),
            BusinessPartyTypeCode=None,
            EORI_No=customs.options.eori_number.state,
        ),
        SpecialService=[
            dhl.SpecialService(
                SpecialServiceType=svc.code,
                ChargeValue=lib.to_money(svc.state),
                CurrencyCode=(
                    currency if lib.to_money(svc.state) is not None else None
                ),
            )
            for svc in option_items
        ],
        Notification=(
            dhl.Notification(
                EmailAddress=options.email_notification_to.state or recipient.email
            )
            if (
                options.email_notification.state
                and any([options.email_notification_to.state, recipient.email])
            )
            else None
        ),
        Place=None,
        EProcShip=None,
        Airwaybill=None,
        DocImages=(
            dhl.DocImages(
                DocImage=[
                    dhl.DocImage(
                        Image=base64.b64decode(doc["doc_file"]),
                        ImageFormat=doc.get("doc_format") or "PDF",
                        Type=provider_units.UploadDocumentType.map(
                            doc.get("doc_type") or "CIN"
                        ).value_or_key,
                    )
                    for doc in options.doc_files.state
                ]
            )
            if (
                options.dhl_paperless_trade.state == True
                and any(options.doc_files.state or [])
            )
            else None
        ),
        LabelImageFormat=label_format,
        RequestArchiveDoc=None,
        NumberOfArchiveDoc=None,
        RequestQRCode="N",
        RequestTransportLabel=None,
        Label=dhl.Label(LabelTemplate=label_template),
        ODDLinkReq=None,
        DGs=None,
        GetPriceEstimate="Y",
        SinglePieceImage="N",
        ShipmentIdentificationNumber=None,
        UseOwnShipmentIdentificationNumber="N",
        Importer=None,
    )

    return lib.Serializable(
        request,
        lambda _: (
            lib.to_xml(
                _,
                name_="req:ShipmentRequest",
                namespacedef_=(
                    'xsi:schemaLocation="http://www.dhl.com '
                    'ship-val-global-req.xsd" '
                    'xmlns:req="http://www.dhl.com" '
                    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
                ),
            )
            .replace('schemaVersion="10"', 'schemaVersion="10.0"')
            .replace("<Image>b'", "<Image>")
            .replace("'</Image>", "</Image>")
        ),
    )
