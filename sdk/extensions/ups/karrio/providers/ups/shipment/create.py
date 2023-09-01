import ups_lib.shipping_response as ups_response
import ups_lib.shipping_request as ups
import time
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.ups.error as provider_error
import karrio.providers.ups.units as provider_units
import karrio.providers.ups.utils as provider_utils


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    details = response.get("ShipmentResponse", {}).get("ShipmentResults")
    shipment = (
        _extract_shipment(details, settings, _response.ctx)
        if details is not None
        else None
    )

    return shipment, provider_error.parse_error_response(response, settings)


def _extract_shipment(
    details: dict,
    settings: provider_utils.Settings,
    ctx: dict,
) -> models.ShipmentDetails:
    label_type = "ZPL" if ctx["label"]["type"] == "ZPL" else "PDF"
    enforce_zpl = settings.connection_config.enforce_zpl.state
    shipment = lib.to_object(ups_response.ShipmentResultsType, details)
    tracking_numbers = [pkg.TrackingNumber for pkg in shipment.PackageResults]
    label = _process_label(shipment)
    zpl_label = None

    if enforce_zpl and label_type == "PDF":
        _label = lib.failsafe(
            lambda: lib.zpl_to_pdf(
                label,
                ctx["label"]["width"],
                ctx["label"]["height"],
                dpmm=8,
            )
        )
        zpl_label = label  # save the original label

        # if the conversion fails, use the original label and label type.
        label = _label or label
        label_type = "ZPL" if _label is None else label_type

    return models.ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=shipment.ShipmentIdentificationNumber,
        shipment_identifier=shipment.ShipmentIdentificationNumber,
        label_type=label_type,
        docs=models.Documents(label=label, zpl_label=zpl_label),
        meta=dict(
            carrier_tracking_link=settings.tracking_url.format(
                shipment.ShipmentIdentificationNumber
            ),
            tracking_numbers=tracking_numbers,
        ),
    )


def _process_label(shipment: ups_response.ShipmentResultsType):
    label_type = (
        "ZPL"
        if "ZPL" in shipment.PackageResults[0].ShippingLabel.ImageFormat.Code
        else "PDF"
    )
    labels = [
        (
            lib.image_to_pdf(
                pkg.ShippingLabel.GraphicImage,
                rotate=-90,
                resize=dict(height=1800, width=1200),
            )
            if label_type == "PDF"
            else pkg.ShippingLabel.GraphicImage
        )
        for pkg in shipment.PackageResults
    ]

    return labels[0] if len(labels) == 1 else lib.bundle_base64(labels, label_type)


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(
        payload.parcels,
        provider_units.PackagePresets,
        package_option_type=provider_units.ShippingOption,
    )
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    weight_unit, dim_unit = packages.compatible_units
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit=weight_unit.value,
    )
    service = provider_units.ServiceCode.map(payload.service)

    payment = payload.payment or models.Payment()
    biling_address = lib.to_address(
        payload.billing_address
        or (payload.shipper if payment.paid_by == "sender" else payload.recipient)
    )
    duty_billing_address = lib.to_address(
        customs.duty_billing_address
        or (payload.shipper if customs.duty.paid_by == "sender" else payload.recipient)
    )

    if any(key in service.value_or_key for key in ["freight", "ground"]):
        packages.validate(required=["weight"])

    country_pair = f"{shipper.country_code}/{recipient.country_code}"
    charges = [
        ("01", payment, biling_address),
        *([("02", customs.duty, duty_billing_address)] if customs is not None else []),
    ]
    indications = [
        *(["01"] if options.pickup_options.state else []),
        *(["02"] if options.delivery_options.state else []),
    ]
    currency = options.currency.state or settings.default_currency
    mps_packaging = (
        provider_units.PackagingType.your_packaging.value if len(packages) > 1 else None
    )
    enforce_zpl = settings.connection_config.enforce_zpl.state
    label_format, label_height, label_width = (
        provider_units.LabelType.map(
            payload.label_type or settings.connection_config.label_type.state
        ).value
        or provider_units.LabelType.PDF_6x4.value
    )

    request = ups.ShippingRequestType(
        ShipmentRequest=ups.ShipmentRequestType(
            Request=ups.RequestType(
                SubVersion="v2205",
                RequestOption="validate",
                TransactionReference=ups.TransactionReferenceType(
                    CustomerContext=payload.reference or "generate label",
                ),
            ),
            Shipment=ups.ShipmentType(
                Description=packages.description,
                ReturnService=None,
                DocumentsOnlyIndicator=("Y" if packages.is_document else None),
                Shipper=ups.ShipperType(
                    Name=(shipper.company_name or shipper.person_name),
                    AttentionName=shipper.contact,
                    CompanyDisplayableName=shipper.company_name,
                    TaxIdentificationNumber=shipper.tax_id,
                    Phone=ups.ShipToPhoneType(
                        Number=shipper.phone_number or "000-000-0000",
                    ),
                    ShipperNumber=settings.account_number,
                    FaxNumber=None,
                    EMailAddress=shipper.email,
                    Address=ups.AlternateDeliveryAddressAddressType(
                        AddressLine=shipper.address_line,
                        City=shipper.city,
                        StateProvinceCode=shipper.state_code,
                        PostalCode=shipper.postal_code,
                        CountryCode=shipper.country_code,
                        ResidentialAddressIndicator=(
                            "Y" if shipper.is_residential else None
                        ),
                    ),
                ),
                ShipTo=ups.ShipToType(
                    Name=(recipient.company_name or recipient.person_name),
                    AttentionName=recipient.contact,
                    CompanyDisplayableName=recipient.company_name,
                    TaxIdentificationNumber=recipient.tax_id,
                    Phone=ups.ShipToPhoneType(
                        Number=recipient.phone_number or "000-000-0000",
                        Extension=None,
                    ),
                    FaxNumber=None,
                    EMailAddress=recipient.email,
                    Address=ups.AlternateDeliveryAddressAddressType(
                        AddressLine=recipient.address_line,
                        City=recipient.city,
                        StateProvinceCode=recipient.state_code,
                        PostalCode=recipient.postal_code,
                        CountryCode=recipient.country_code,
                        ResidentialAddressIndicator=(
                            "Y" if recipient.is_residential else None
                        ),
                    ),
                    LocationID=None,
                ),
                AlternateDeliveryAddress=None,
                ShipFrom=ups.ShipFromType(
                    Name=(shipper.company_name or shipper.person_name),
                    AttentionName=shipper.contact,
                    CompanyDisplayableName=shipper.company_name,
                    TaxIdentificationNumber=shipper.tax_id,
                    Phone=ups.ShipFromPhoneType(
                        Number=shipper.phone_number or "000-000-0000",
                    ),
                    FaxNumber=None,
                    Address=ups.AlternateDeliveryAddressAddressType(
                        AddressLine=shipper.address_line,
                        City=shipper.city,
                        StateProvinceCode=shipper.state_code,
                        PostalCode=shipper.postal_code,
                        CountryCode=shipper.country_code,
                        ResidentialAddressIndicator=(
                            "Y" if shipper.is_residential else None
                        ),
                    ),
                    VendorInfo=None,
                ),
                PaymentInformation=ups.PaymentInformationType(
                    ShipmentCharge=[
                        ups.ShipmentChargeType(
                            Type=charge_type,
                            BillShipper=(
                                ups.BillShipperType(
                                    AccountNumber=(
                                        payment.account_number
                                        or settings.account_number
                                    ),
                                    CreditCard=None,
                                    AlternatePaymentMethod=None,
                                )
                                if payment.paid_by == "sender"
                                else None
                            ),
                            BillReceiver=(
                                ups.BillReceiverType(
                                    AccountNumber=payment.account_number,
                                    Address=ups.BillReceiverAddressType(
                                        PostalCode=billing_address.postal_code,
                                    ),
                                )
                                if payment.paid_by == "recipient"
                                else None
                            ),
                            BillThirdParty=(
                                ups.BillThirdPartyType(
                                    AccountNumber=payment.account_number,
                                    CertifiedElectronicMail=None,
                                    InterchangeSystemCode=None,
                                    FRSPaymentInformation=None,
                                )
                                if payment.paid_by == "third_party"
                                else None
                            ),
                            ConsigneeBilledIndicator=(
                                "Y" if payment.paid_by == "recipient" else None
                            ),
                        )
                        for charge_type, payment, billing_address in charges
                    ],
                    SplitDutyVATIndicator=None,
                ),
                FRSPaymentInformation=None,
                FreightShipmentInformation=None,
                GoodsNotInFreeCirculationIndicator=None,
                PromotionalDiscountInformation=None,
                DGSignatoryInfo=None,
                ShipmentRatingOptions=ups.ShipmentRatingOptionsType(
                    NegotiatedRatesIndicator="Y",
                    FRSShipmentIndicator=None,
                    RateChartIndicator=None,
                    UserLevelDiscountIndicator=None,
                    TPFCNegotiatedRatesIndicator=None,
                ),
                MovementReferenceNumber=None,
                ReferenceNumber=(
                    ups.ReferenceNumberType(
                        BarCodeIndicator=None,
                        Code=shipper.country_code,
                        Value=payload.reference,
                    )
                    if (country_pair not in ["US/US", "PR/PR"])
                    and any(payload.reference or "")
                    else None
                ),
                Service=ups.LabelImageFormatType(
                    Code=service.value_or_key,
                    Description=service.name_or_key,
                ),
                InvoiceLineTotal=ups.InvoiceLineTotalType(
                    CurrencyCode=currency,
                    MonetaryValue=str(
                        options.declared_value.state
                        or packages.items.value_amount
                        or 1.0
                    ),
                ),
                NumOfPiecesInShipment=str(packages.items.quantity),
                USPSEndorsement=None,
                MILabelCN22Indicator=None,
                SubClassification=None,
                CostCenter=(
                    options.cost_center.state
                    or settings.connection_config.cost_center.state
                ),
                CostCenterBarcodeIndicator=(
                    "Y"
                    if (
                        options.cost_center.state
                        or settings.connection_config.cost_center.state
                    )
                    else None
                ),
                PackageID=None,
                PackageIDBarcodeIndicator=None,
                IrregularIndicator=None,
                ShipmentIndicationType=[
                    ups.LabelImageFormatType(Code=code, Description="Indicator")
                    for code in indications
                ],
                MIDualReturnShipmentKey=None,
                RatingMethodRequestedIndicator="Y",
                TaxInformationIndicator="Y",
                ShipmentServiceOptions=(
                    ups.ShipmentServiceOptionsType(
                        SaturdayPickupIndicator=(
                            "Y" if options.ups_saturday_pickup.state else None
                        ),
                        SaturdayDeliveryIndicator=(
                            "Y" if options.ups_saturday_delivery.state else None
                        ),
                        COD=(
                            ups.CodType(
                                CODFundsCode="0",  # TODO: find reference
                                CODAmount=ups.InvoiceLineTotalType(
                                    CurrencyCode=options.currency.state,
                                    MonetaryValue=str(options.cash_on_delivery.state),
                                ),
                            )
                            if options.cash_on_delivery.state
                            else None
                        ),
                        AccessPointCOD=(
                            ups.InvoiceLineTotalType(
                                CurrencyCode=options.currency.state,
                                MonetaryValue=lib.to_money(
                                    options.ups_access_point_cod.state
                                ),
                            )
                            if options.ups_access_point_cod.state
                            else None
                        ),
                        DeliverToAddresseeOnlyIndicator=None,
                        DirectDeliveryOnlyIndicator=None,
                        Notification=(
                            [
                                ups.NotificationElementType(
                                    NotificationCode=event,
                                    EMail=ups.MailType(
                                        EMailAddress=(
                                            options.email_notification_to.state
                                            or recipient.email
                                        ),
                                        UndeliverableEMailAddress=None,
                                        FromEMailAddress=None,
                                        FromName=None,
                                        Memo=None,
                                        Subject=None,
                                        SubjectCode=None,
                                    ),
                                    VoiceMessage=None,
                                    TextMessage=None,
                                    Locale=None,
                                )
                                for event in ["8"]
                            ]
                            if options.email_notification.state
                            and any(
                                [
                                    options.email_notification_to.state,
                                    recipient.email,
                                ]
                            )
                            else []
                        ),
                        LabelDelivery=None,
                        InternationalForms=(
                            ups.InternationalFormsType(
                                FormType=(
                                    "07" if options.paperless_trade.state else "01"
                                ),
                                UserCreatedForm=[
                                    ups.UserCreatedFormType(DocumentID=doc["doc_id"])
                                    for doc in (options.doc_references.state or [])
                                ],
                                UPSPremiumCareForm=None,
                                CN22Form=None,
                                AdditionalDocumentIndicator=None,
                                FormGroupIdName=None,
                                EEIFilingOption=None,
                                Contacts=(
                                    ups.ContactsType(
                                        ForwardAgent=None,
                                        UltimateConsignee=None,
                                        IntermediateConsignee=None,
                                        Producer=None,
                                        SoldTo=ups.ProducerType(
                                            Option=None,
                                            CompanyName=recipient.company_name,
                                            Name=recipient.contact,
                                            AttentionName=recipient.contact,
                                            TaxIdentificationNumber=recipient.tax_id,
                                            Phone=ups.ShipToPhoneType(
                                                Number=recipient.phone_number
                                                or "000-000-0000"
                                            ),
                                            Address=ups.AlternateDeliveryAddressAddressType(
                                                AddressLine=recipient.address_line,
                                                City=recipient.city,
                                                StateProvinceCode=recipient.state_code,
                                                PostalCode=lib.text(
                                                    (
                                                        recipient.postal_code or ""
                                                    ).replace("-", "")
                                                ),
                                                CountryCode=recipient.country_code,
                                                ResidentialAddressIndicator=(
                                                    "Y"
                                                    if recipient.is_residential
                                                    else None
                                                ),
                                                Town=None,
                                            ),
                                            EMailAddress=recipient.email,
                                        ),
                                    )
                                    if not options.paperless_trade.state
                                    else None
                                ),
                                Product=[
                                    ups.ProductType(
                                        Description=lib.text(
                                            item.title or item.description,
                                            max=35,
                                        ),
                                        Unit=ups.UnitType(
                                            Number=str(item.quantity),
                                            UnitOfMeasurement=ups.LabelImageFormatType(
                                                Code="PCS",
                                                Description="PCS",
                                            ),
                                            Value=str(item.value_amount),
                                        ),
                                        CommodityCode=item.hs_code,
                                        PartNumber=item.sku,
                                        OriginCountryCode=item.origin_country,
                                        JointProductionIndicator=None,
                                        NetCostCode=None,
                                        NetCostDateRange=None,
                                        PreferenceCriteria=None,
                                        ProducerInfo=None,
                                        MarksAndNumbers=None,
                                        NumberOfPackagesPerCommodity="1",
                                        ProductWeight=ups.WeightType(
                                            UnitOfMeasurement=ups.LabelImageFormatType(
                                                Code=provider_units.WeightUnit.map(
                                                    weight_unit.name
                                                ).value,
                                                Description="weight unit",
                                            ),
                                            Weight=str(
                                                units.Weight(
                                                    item.weight, weight_unit.name
                                                )[weight_unit.name]
                                            ),
                                        ),
                                        VehicleID=None,
                                        ScheduleB=None,
                                        ExportType="F",
                                        SEDTotalValue=None,
                                        ExcludeFromForm=None,
                                        PackingListInfo=None,
                                        EEIInformation=None,
                                    )
                                    for idx, item in enumerate(customs.commodities)
                                ],
                                InvoiceNumber=customs.invoice,
                                InvoiceDate=lib.fdatetime(
                                    customs.invoice_date
                                    or time.strftime("%Y-%m-%d", time.localtime()),
                                    current_format="%Y-%m-%d",
                                    output_format="%Y%m%d",
                                ),
                                PurchaseOrderNumber=None,
                                TermsOfShipment=provider_units.Incoterm.map(
                                    customs.incoterm
                                ).name,
                                ReasonForExport=provider_units.CustomsContentType.map(
                                    customs.content_type
                                ).value,
                                Comments=None,
                                DeclarationStatement="I hereby certify that the information on this invoice is true and correct and the contents and value of this shipment is as stated above.",
                                Discount=None,
                                FreightCharges=None,
                                InsuranceCharges=(
                                    ups.DiscountType(
                                        MonetaryValue=options.insurance.state,
                                    )
                                    if options.insurance.state is not None
                                    else None
                                ),
                                OtherCharges=None,
                                CurrencyCode=(
                                    customs.duty.currency or options.currency.state
                                ),
                                BlanketPeriod=None,
                                ExportDate=None,
                                ExportingCarrier=None,
                                CarrierID=None,
                                InBondCode=None,
                                EntryNumber=None,
                                PointOfOrigin=None,
                                PointOfOriginType=None,
                                ModeOfTransport=None,
                                PortOfExport=None,
                                PortOfUnloading=None,
                                PartiesToTransaction=None,
                                RoutedExportTransactionIndicator=None,
                                ContainerizedIndicator=None,
                                OverridePaperlessIndicator=None,
                                ShipperMemo=None,
                                HazardousMaterialsIndicator=None,
                            )
                            if payload.customs
                            else None
                        ),
                        DeliveryConfirmation=None,
                        ReturnOfDocumentIndicator=None,
                        ImportControlIndicator=None,
                        LabelMethod=None,
                        CommercialInvoiceRemovalIndicator=None,
                        UPScarbonneutralIndicator=None,
                        ExchangeForwardIndicator=None,
                        HoldForPickupIndicator=None,
                        DropoffAtUPSFacilityIndicator=None,
                        LiftGateForPickupIndicator=None,
                        LiftGateForDeliveryIndicator=None,
                        SDLShipmentIndicator=None,
                        EPRAReleaseCode=None,
                        RestrictedArticles=None,
                        InsideDelivery=None,
                        ItemDisposal=None,
                    )
                ),
                ShipmentValueThresholdCode=None,
                MasterCartonID=None,
                MasterCartonIndicator=None,
                BarCodeImageIndicator=None,
                ShipmentDate=None,
                Package=[
                    ups.PackageType(
                        Packaging=ups.LabelImageFormatType(
                            Code=(
                                mps_packaging
                                or provider_units.PackagingType.map(
                                    package.packaging_type
                                ).value
                                or provider_units.PackagingType.ups_customer_supplied_package.value
                            ),
                            Description="Packaging Type",
                        ),
                        Dimensions=(
                            ups.DimensionsType(
                                UnitOfMeasurement=ups.LabelImageFormatType(
                                    Code=package.dimension_unit.value,
                                    Description="Dimension",
                                ),
                                Length=str(package.length.value),
                                Width=str(package.width.value),
                                Height=str(package.height.value),
                            )
                            if any([package.length, package.width, package.height])
                            else None
                        ),
                        DimWeight=None,
                        PackageWeight=ups.WeightType(
                            UnitOfMeasurement=ups.LabelImageFormatType(
                                Code=provider_units.WeightUnit[
                                    str(package.weight.unit)
                                ].value,
                                Description="Weight",
                            ),
                            Weight=str(package.weight.value),
                        ),
                        Commodity=None,
                        PackageServiceOptions=None,
                        UPSPremier=None,
                    )
                    for package in packages
                ],
            ),
            LabelSpecification=ups.LabelSpecificationType(
                LabelImageFormat=ups.LabelImageFormatType(
                    Code="ZPL" if enforce_zpl else label_format,
                    Description="lable format",
                ),
                HTTPUserAgent=None,
                LabelStockSize=ups.LabelStockSizeType(
                    Height=str(label_height),
                    Width=str(label_width),
                ),
            ),
            ReceiptSpecification=None,
        )
    )

    return lib.Serializable(
        request,
        lib.to_dict,
        dict(
            label=dict(
                height=label_height,
                width=label_width,
                type=label_format,
            ),
        ),
    )
