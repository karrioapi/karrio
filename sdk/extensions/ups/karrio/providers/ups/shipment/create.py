import ups_lib.ship_web_service_schema as ups
import ups_lib.common as common
import time
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.ups.error as provider_error
import karrio.providers.ups.units as provider_units
import karrio.providers.ups.utils as provider_utils


def parse_shipment_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    details = lib.find_element("ShipmentResults", response, first=True)
    shipment = (
        _extract_shipment(details, settings, _response.ctx)
        if details is not None
        else None
    )

    return shipment, provider_error.parse_error_response(response, settings)


def _extract_shipment(
    node: lib.Element,
    settings: provider_utils.Settings,
    ctx: dict,
) -> models.ShipmentDetails:
    label_type = "ZPL" if ctx["label"]["type"] == "ZPL" else "PDF"
    enforce_zpl = settings.connection_config.enforce_zpl.state
    shipment = lib.to_object(ups.ShipmentResultsType, node)
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
        ),
    )


def _process_label(shipment: ups.ShipmentResultsType):
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
    service = provider_units.ServiceCode.map(payload.service).value_or_key

    payment = payload.payment or models.Payment()
    biling_address = lib.to_address(
        payload.billing_address
        or (payload.shipper if payment.paid_by == "sender" else payload.recipient)
    )
    duty_billing_address = lib.to_address(
        customs.duty_billing_address
        or (payload.shipper if customs.duty.paid_by == "sender" else payload.recipient)
    )

    if any(key in service for key in ["freight", "ground"]):
        packages.validate(required=["weight"])

    country_pair = f"{shipper.country_code}/{recipient.country_code}"
    charges = (
        [("01", payment, biling_address)]
        if payload.customs is None
        else [
            ("01", payment, biling_address),
            ("02", customs.duty, duty_billing_address),
        ]
    )
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

    request = lib.Envelope(
        Header=lib.Header(
            settings.Security,
        ),
        Body=lib.Body(
            ups.ShipmentRequest(
                Request=common.RequestType(
                    RequestOption=["validate"],
                    SubVersion=None,
                    TransactionReference=common.TransactionReferenceType(
                        CustomerContext=payload.reference,
                        TransactionIdentifier=getattr(payload, "id", None),
                    ),
                ),
                Shipment=ups.ShipmentType(
                    Description=packages.description,
                    DocumentsOnlyIndicator=("" if packages.is_document else None),
                    Shipper=ups.ShipperType(
                        Name=(shipper.company_name or shipper.person_name),
                        AttentionName=shipper.person_name,
                        CompanyDisplayableName=shipper.company_name,
                        TaxIdentificationNumber=shipper.federal_tax_id,
                        TaxIDType=None,
                        Phone=ups.ShipPhoneType(
                            Number=shipper.phone_number or "000-000-0000"
                        ),
                        ShipperNumber=settings.account_number,
                        FaxNumber=None,
                        EMailAddress=shipper.email,
                        Address=ups.ShipAddressType(
                            AddressLine=shipper.address_lines,
                            City=shipper.city,
                            StateProvinceCode=shipper.state_code,
                            PostalCode=shipper.postal_code,
                            CountryCode=shipper.country_code,
                        ),
                    ),
                    ShipFrom=ups.ShipperType(
                        Name=(shipper.company_name or shipper.person_name),
                        AttentionName=shipper.person_name,
                        CompanyDisplayableName=shipper.company_name,
                        TaxIdentificationNumber=shipper.federal_tax_id,
                        TaxIDType=None,
                        Phone=ups.ShipPhoneType(
                            Number=shipper.phone_number or "000-000-0000"
                        ),
                        ShipperNumber=settings.account_number,
                        FaxNumber=None,
                        EMailAddress=shipper.email,
                        Address=ups.ShipAddressType(
                            AddressLine=shipper.address_lines,
                            City=shipper.city,
                            StateProvinceCode=shipper.state_code,
                            PostalCode=shipper.postal_code,
                            CountryCode=shipper.country_code,
                        ),
                    ),
                    ShipTo=ups.ShipToType(
                        Name=(recipient.company_name or recipient.person_name),
                        AttentionName=recipient.person_name,
                        CompanyDisplayableName=recipient.company_name,
                        TaxIdentificationNumber=recipient.federal_tax_id,
                        TaxIDType=None,
                        Phone=ups.ShipPhoneType(
                            Number=recipient.phone_number or "000-000-0000"
                        ),
                        FaxNumber=None,
                        EMailAddress=recipient.email,
                        Address=ups.ShipAddressType(
                            AddressLine=recipient.address_lines,
                            City=recipient.city,
                            StateProvinceCode=recipient.state_code,
                            PostalCode=recipient.postal_code,
                            CountryCode=recipient.country_code,
                        ),
                    ),
                    PaymentInformation=ups.PaymentInfoType(
                        ShipmentCharge=[
                            ups.ShipmentChargeType(
                                Type=charge_type,
                                BillShipper=(
                                    ups.BillShipperType(
                                        AccountNumber=settings.account_number,
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
                                            PostalCode=address.postal_code,
                                        ),
                                    )
                                    if payment.paid_by == "recipient"
                                    else None
                                ),
                                BillThirdParty=(
                                    ups.BillThirdPartyChargeType(
                                        AccountNumber=payment.account_number,
                                        Address=ups.AccountAddressType(
                                            PostalCode=address.postal_code,
                                            CountryCode=address.country_code,
                                        ),
                                    )
                                    if payment.paid_by == "third_party"
                                    else None
                                ),
                                ConsigneeBilledIndicator=None,
                            )
                            for charge_type, payment, address in charges
                        ],
                        SplitDutyVATIndicator=None,
                    ),
                    MovementReferenceNumber=None,
                    ReferenceNumber=(
                        [
                            ups.ReferenceNumberType(
                                BarCodeIndicator=None,
                                Code=shipper.country_code,
                                Value=payload.reference,
                            )
                        ]
                        if (country_pair not in ["US/US", "PR/PR"])
                        and any(payload.reference or "")
                        else None
                    ),
                    Service=(
                        ups.ServiceType(Code=service) if service is not None else None
                    ),
                    ShipmentServiceOptions=ups.ShipmentServiceOptionsType(
                        SaturdayPickupIndicator=(
                            "" if options.ups_saturday_pickup_indicator.state else None
                        ),
                        SaturdayDeliveryIndicator=(
                            ""
                            if options.ups_saturday_delivery_indicator.state
                            else None
                        ),
                        COD=(
                            ups.CODType(
                                CODFundsCode=None,
                                CODAmount=ups.CurrencyMonetaryType(
                                    CurrencyCode=options.currency.state or "USD",
                                    MonetaryValue=options.cash_on_delivery.state,
                                ),
                            )
                            if options.cash_on_delivery.state
                            else None
                        ),
                        AccessPointCOD=(
                            ups.ShipmentServiceOptionsAccessPointCODType(
                                CurrencyCode=options.currency.state,
                                MonetaryValue=lib.to_money(
                                    options.ups_access_point_cod.state
                                ),
                            )
                            if options.ups_access_point_cod.state
                            else None
                        ),
                        DeliverToAddresseOnlyIndicator=(
                            ""
                            if options.ups_deliver_to_addressee_only_indicator.state
                            else None
                        ),
                        DirectDeliveryOnlyIndicator=(
                            ""
                            if options.ups_direct_delivery_only_indicator.state
                            else None
                        ),
                        Notification=(
                            [
                                ups.NotificationType(
                                    NotificationCode=event,
                                    EMail=ups.EmailDetailsType(
                                        EMailAddress=[
                                            options.email_notification_to.state
                                            or recipient.email
                                        ]
                                    ),
                                    VoiceMessage=None,
                                    TextMessage=None,
                                    Locale=None,
                                )
                                for event in [8]
                            ]
                            if options.email_notification.state
                            and any(
                                [
                                    options.email_notification_to.state,
                                    recipient.email,
                                ]
                            )
                            else None
                        ),
                        LabelDelivery=None,
                        InternationalForms=(
                            ups.InternationalFormType(
                                FormType=(
                                    ["07"] if options.paperless_trade.state else ["01"]
                                ),
                                UserCreatedForm=(
                                    ups.UserCreatedFormType(
                                        DocumentID=[
                                            doc["doc_id"]
                                            for doc in options.doc_references.state
                                        ]
                                    )
                                    if any(options.doc_references.state or [])
                                    else None
                                ),
                                CN22Form=None,
                                UPSPremiumCareForm=None,
                                AdditionalDocumentIndicator=None,
                                FormGroupIdName=None,
                                SEDFilingOption=None,
                                EEIFilingOption=None,
                                Contacts=(
                                    ups.ContactType(
                                        ForwardAgent=None,
                                        UltimateConsignee=None,
                                        IntermediateConsignee=None,
                                        Producer=None,
                                        SoldTo=ups.SoldToType(
                                            Name=(
                                                recipient.company_name
                                                or recipient.person_name
                                            ),
                                            AttentionName=(
                                                recipient.person_name
                                                or recipient.company_name
                                            ),
                                            TaxIdentificationNumber=recipient.tax_id,
                                            Phone=ups.ShipPhoneType(
                                                Number=recipient.phone_number
                                                or "000-000-0000"
                                            ),
                                            Option=None,
                                            Address=ups.AddressType(
                                                AddressLine=recipient.address_lines,
                                                City=recipient.city,
                                                StateProvinceCode=recipient.state_code,
                                                PostalCode=lib.text(
                                                    (
                                                        recipient.postal_code or ""
                                                    ).replace("-", "")
                                                ),
                                                CountryCode=recipient.country_code,
                                            ),
                                            EMailAddress=recipient.email,
                                        ),
                                    )
                                    if not options.paperless_trade.state
                                    else None
                                ),
                                Product=[
                                    ups.ProductType(
                                        Description=[
                                            lib.text(
                                                item.title or item.description,
                                                max=35,
                                            )
                                        ],
                                        Unit=ups.UnitType(
                                            Number=str(item.quantity),
                                            UnitOfMeasurement=ups.UnitOfMeasurementType(
                                                Code="PCS"
                                            ),
                                            Value=item.value_amount,
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
                                        NumberOfPackagesPerCommodity=1,
                                        ProductWeight=ups.ProductWeightType(
                                            UnitOfMeasurement=ups.UnitOfMeasurementType(
                                                Code=provider_units.WeightUnit.map(
                                                    weight_unit.name
                                                ).value,
                                            ),
                                            Weight=units.Weight(
                                                item.weight, weight_unit.name
                                            )[weight_unit.name],
                                        ),
                                        VehicleID=None,
                                        ScheduleB=None,
                                        ExportType="F",
                                        SEDTotalValue=None,
                                        ExcludeFromForm=None,
                                        ProductCurrencyCode=None,
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
                                    ups.IFChargesType(
                                        MonetaryValue=options.insurance.state
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
                                License=None,
                                ECCNNumber=None,
                                OverridePaperlessIndicator=None,
                                ShipperMemo=None,
                                MultiCurrencyInvoiceLineTotal=None,
                                HazardousMaterialsIndicator=None,
                            )
                            if payload.customs
                            else None
                        ),
                        DeliveryConfirmation=(
                            ups.DeliveryConfirmationType(
                                DCISType=options.ups_delivery_confirmation.state or "01"
                            )
                            if options.ups_delivery_confirmation.state
                            else None
                        ),
                        ReturnOfDocumentIndicator=(
                            ""
                            if options.ups_return_of_document_indicator.state
                            else None
                        ),
                        ImportControlIndicator=(
                            "" if options.ups_import_control_indicator.state else None
                        ),
                        LabelMethod=None,
                        CommercialInvoiceRemovalIndicator=(
                            ""
                            if options.ups_commercial_invoice_removal_indicator.state
                            else None
                        ),
                        UPScarbonneutralIndicator=(
                            "" if options.ups_carbonneutral_indicator.state else None
                        ),
                        PreAlertNotification=None,
                        ExchangeForwardIndicator=None,
                        HoldForPickupIndicator=(
                            "" if options.ups_hold_for_pickup_indicator.state else None
                        ),
                        DropoffAtUPSFacilityIndicator=(
                            ""
                            if options.ups_drop_off_at_ups_facility_indicator.state
                            else None
                        ),
                        LiftGateForPickUpIndicator=(
                            ""
                            if options.ups_lift_gate_at_pickup_indicator.state
                            else None
                        ),
                        LiftGateForDeliveryIndicator=(
                            ""
                            if options.ups_lift_gate_at_delivery_indicator.state
                            else None
                        ),
                        SDLShipmentIndicator=(
                            "" if options.ups_sdl_shipment_indicator.state else None
                        ),
                        EPRAReleaseCode=(
                            "" if options.ups_epra_indicator.state else None
                        ),
                        RestrictedArticles=None,
                        InsideDelivery=None,
                        ItemDisposal=None,
                    ),
                    Package=[
                        ups.PackageType(
                            Description=package.parcel.description,
                            Packaging=ups.PackagingType(
                                Code=(
                                    mps_packaging
                                    or provider_units.PackagingType.map(
                                        package.packaging_type
                                    ).value
                                    or provider_units.PackagingType.ups_customer_supplied_package.value
                                ),
                            ),
                            Dimensions=ups.DimensionsType(
                                UnitOfMeasurement=ups.ShipUnitOfMeasurementType(
                                    Code=dim_unit.value,
                                ),
                                Length=package.length.value,
                                Width=package.width.value,
                                Height=package.height.value,
                            ),
                            PackageWeight=ups.PackageWeightType(
                                UnitOfMeasurement=ups.ShipUnitOfMeasurementType(
                                    Code=provider_units.WeightUnit[
                                        weight_unit.name
                                    ].value,
                                ),
                                Weight=package.weight.value,
                            ),
                        )
                        for package in packages
                    ],
                ),
                LabelSpecification=ups.LabelSpecificationType(
                    LabelImageFormat=ups.LabelImageFormatType(
                        Code="ZPL" if enforce_zpl else label_format
                    ),
                    HTTPUserAgent=None,
                    LabelStockSize=ups.LabelStockSizeType(
                        Height=label_height,
                        Width=label_width,
                    ),
                    Instruction=None,
                    CharacterSet=None,
                ),
                ReceiptSpecification=None,
            ),
        ),
    )

    return lib.Serializable(
        request,
        lambda envelope: lib.envelope_serializer(
            envelope,
            namespace=(
                'xmlns:auth="http://www.ups.com/schema/xpci/1.0/auth"'
                ' xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"'
                ' xmlns:xsd="http://www.w3.org/2001/XMLSchema"'
                ' xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0"'
                ' xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0"'
                ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
                ' xsi:schemaLocation="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0"'
                ' xmlns:ship="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0"'
                ' xmlns:ifs="http://www.ups.com/XMLSchema/XOLTWS/IF/v1.0"'
            ),
            prefixes=dict(
                Request="common",
                Envelope="soapenv",
                UPSSecurity="upss",
                ShipmentRequest="ship",
                InternationalForms_children="ifs",
            ),
        ),
        dict(
            label=dict(
                height=label_height,
                width=label_width,
                type=label_format,
            ),
        ),
    )
