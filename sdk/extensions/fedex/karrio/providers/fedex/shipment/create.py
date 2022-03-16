from datetime import datetime
from typing import List, Tuple
from fedex_lib.ship_service_v26 import (
    ProcessShipmentRequest,
    TransactionDetail,
    VersionId,
    RequestedShipment,
    RequestedPackageLineItem,
    Party,
    Contact,
    Address,
    TaxpayerIdentification,
    Weight as FedexWeight,
    Dimensions as FedexDimensions,
    TrackingId,
    ShipmentSpecialServicesRequested,
    ShipmentEventNotificationDetail,
    ShipmentEventNotificationSpecification,
    NotificationDetail,
    EMailDetail,
    Localization,
    CodDetail,
    CodCollectionType,
    Money,
    Payment,
    Payor,
    LabelSpecification,
    LabelFormatType,
    LabelPrintingOrientationType,
    ShipmentNotificationFormatSpecification,
    LabelOrderType,
    CustomsClearanceDetail,
    Commodity,
    CommercialInvoice,
    CustomerReference,
    CustomerReferenceType,
    ShippingDocumentSpecification,
    CommercialInvoiceDetail,
    ShippingDocumentFormat,
)
from karrio.core.utils import (
    Serializable,
    apply_namespaceprefix,
    create_envelope,
    bundle_base64,
    Element,
    XP,
    DF,
)
from karrio.core.units import Options, Packages, CompleteAddress, Weight
from karrio.core.models import (
    Documents,
    Duty,
    ShipmentDetails,
    Message,
    ShipmentRequest,
)
from karrio.providers.fedex.error import parse_error_response
from karrio.providers.fedex.utils import Settings
from karrio.providers.fedex.units import (
    PackagingType,
    ServiceType,
    SpecialServiceType,
    PackagePresets,
    PaymentType,
    LabelType,
    Incoterm,
    PurposeType,
    MeasurementOptions,
)


NOTIFICATION_EVENTS = [
    "ON_DELIVERY",
    "ON_ESTIMATED_DELIVERY",
    "ON_EXCEPTION",
    "ON_SHIPMENT",
    "ON_TENDER",
]


def parse_shipment_response(
    response: Element, settings: Settings
) -> Tuple[ShipmentDetails, List[Message]]:
    details = XP.find("CompletedPackageDetails", response)
    documents = XP.find("ShipmentDocuments", response)

    shipment = (
        _extract_shipment((details, documents), settings) if len(details) > 0 else None
    )
    return shipment, parse_error_response(response, settings)


def _extract_shipment(
    details: Tuple[List[Element], List[Element]], settings: Settings
) -> ShipmentDetails:
    pieces, docs = details
    tracking_numbers = [
        getattr(XP.find("TrackingNumber", piece, first=True), "text", None)
        for piece in pieces
    ]
    [master_id, *_] = tracking_numbers

    labels = [
        getattr(XP.find("Image", piece, first=True), "text", None) for piece in pieces
    ]
    label_type = getattr(XP.find("ImageType", pieces[0], first=True), "text", None)

    invoices = [
        getattr(XP.find("Image", doc, first=True), "text", None) for doc in docs
    ]
    doc_type = (
        getattr(XP.find("ImageType", docs[0], first=True), "text", None)
        if len(docs) > 0
        else "PDF"
    )

    label = labels[0] if len(labels) == 1 else bundle_base64(labels, label_type)
    invoice = invoices[0] if len(invoices) == 1 else bundle_base64(invoices, doc_type)

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=master_id,
        shipment_identifier=master_id,
        docs=Documents(
            label=label,
            **({"invoice": invoice} if invoice else {}),
        ),
        meta=dict(tracking_numbers=tracking_numbers),
    )


def shipment_request(
    payload: ShipmentRequest, settings: Settings
) -> Serializable[ProcessShipmentRequest]:
    shipper = CompleteAddress.map(payload.shipper)
    recipient = CompleteAddress.map(payload.recipient)
    packages = Packages(payload.parcels, PackagePresets, required=["weight"])

    service = ServiceType.map(payload.service).value_or_key
    options = Options(payload.options, SpecialServiceType)
    special_services = [
        getattr(v, "value", v) for k, v in options if k in SpecialServiceType
    ]
    label_type, label_format = LabelType[payload.label_type or "PDF_4x6"].value
    customs = payload.customs
    duty = (customs.duty or Duty(paid_by="sender")) if customs is not None else None
    bill_to = CompleteAddress(getattr(duty, "bill_to", None))

    requests = [
        ProcessShipmentRequest(
            WebAuthenticationDetail=settings.webAuthenticationDetail,
            ClientDetail=settings.clientDetail,
            TransactionDetail=TransactionDetail(CustomerTransactionId="IE_v26_Ship"),
            Version=VersionId(ServiceId="ship", Major=26, Intermediate=0, Minor=0),
            RequestedShipment=RequestedShipment(
                ShipTimestamp=DF.date(options.shipment_date or datetime.now()),
                DropoffType="REGULAR_PICKUP",
                ServiceType=service,
                PackagingType=PackagingType.map(
                    packages.package_type or "your_packaging"
                ).value,
                ManifestDetail=None,
                VariationOptions=None,
                TotalWeight=FedexWeight(
                    Units=packages.weight.unit, Value=packages.weight.value
                ),
                TotalInsuredValue=options.insurance,
                PreferredCurrency=options.currency,
                ShipmentAuthorizationDetail=None,
                Shipper=Party(
                    AccountNumber=settings.account_number,
                    Tins=(
                        [TaxpayerIdentification(Number=tax) for tax in shipper.taxes]
                        if shipper.has_tax_info
                        else None
                    ),
                    Contact=(
                        Contact(
                            ContactId=None,
                            PersonName=shipper.person_name,
                            Title=None,
                            CompanyName=shipper.company_name,
                            PhoneNumber=shipper.phone_number,
                            PhoneExtension=None,
                            TollFreePhoneNumber=None,
                            PagerNumber=None,
                            FaxNumber=None,
                            EMailAddress=shipper.email,
                        )
                        if shipper.has_contact_info
                        else None
                    ),
                    Address=Address(
                        StreetLines=shipper.address_lines,
                        City=shipper.city,
                        StateOrProvinceCode=shipper.state_code,
                        PostalCode=shipper.postal_code,
                        UrbanizationCode=None,
                        CountryCode=shipper.country_code,
                        CountryName=shipper.country_name,
                        Residential=shipper.residential,
                        GeographicCoordinates=None,
                    ),
                ),
                Recipient=Party(
                    AccountNumber=None,
                    Tins=(
                        [TaxpayerIdentification(Number=tax) for tax in recipient.taxes]
                        if recipient.has_tax_info
                        else None
                    ),
                    Contact=(
                        Contact(
                            ContactId=None,
                            PersonName=recipient.person_name,
                            Title=None,
                            CompanyName=recipient.company_name,
                            PhoneNumber=recipient.phone_number,
                            PhoneExtension=None,
                            TollFreePhoneNumber=None,
                            PagerNumber=None,
                            FaxNumber=None,
                            EMailAddress=recipient.email,
                        )
                        if recipient.has_contact_info
                        else None
                    ),
                    Address=Address(
                        StreetLines=recipient.address_lines,
                        City=recipient.city,
                        StateOrProvinceCode=recipient.state_code,
                        PostalCode=recipient.postal_code,
                        UrbanizationCode=None,
                        CountryCode=recipient.country_code,
                        CountryName=recipient.country_name,
                        Residential=recipient.residential,
                        GeographicCoordinates=None,
                    ),
                ),
                RecipientLocationNumber=None,
                Origin=None,
                SoldTo=None,
                ShippingChargesPayment=Payment(
                    PaymentType=PaymentType[payload.payment.paid_by or "sender"].value,
                    Payor=Payor(
                        ResponsibleParty=Party(
                            AccountNumber=(
                                payload.payment.account_number
                                or settings.account_number
                            ),
                        )
                    ),
                ),
                SpecialServicesRequested=(
                    ShipmentSpecialServicesRequested(
                        SpecialServiceTypes=special_services,
                        CodDetail=(
                            CodDetail(
                                CodCollectionAmount=Money(
                                    Currency=options.currency or "USD",
                                    Amount=options.cash_on_delivery,
                                ),
                                AddTransportationChargesDetail=None,
                                CollectionType=CodCollectionType.CASH,
                                CodRecipient=None,
                                FinancialInstitutionContactAndAddress=None,
                                RemitToName=None,
                                ReferenceIndicator=None,
                                ReturnTrackingId=None,
                            )
                            if options.cash_on_delivery
                            else None
                        ),
                        DeliveryOnInvoiceAcceptanceDetail=None,
                        HoldAtLocationDetail=None,
                        EventNotificationDetail=(
                            ShipmentEventNotificationDetail(
                                AggregationType=None,
                                PersonalMessage=None,
                                EventNotifications=[
                                    ShipmentEventNotificationSpecification(
                                        Role=None,
                                        Events=NOTIFICATION_EVENTS,
                                        NotificationDetail=NotificationDetail(
                                            NotificationType="EMAIL",
                                            EmailDetail=EMailDetail(
                                                EmailAddress=(
                                                    options.email_notification_to
                                                    or recipient.email
                                                ),
                                                Name=recipient.person_name
                                                or recipient.company_name,
                                            ),
                                            Localization=Localization(
                                                LanguageCode="EN"
                                            ),
                                        ),
                                        FormatSpecification=ShipmentNotificationFormatSpecification(
                                            Type="TEXT"
                                        ),
                                    )
                                ],
                            )
                            if options.email_notification
                            and any([options.email_notification_to, recipient.email])
                            else None
                        ),
                        ReturnShipmentDetail=None,
                        PendingShipmentDetail=None,
                        InternationalControlledExportDetail=None,
                        InternationalTrafficInArmsRegulationsDetail=None,
                        ShipmentDryIceDetail=None,
                        HomeDeliveryPremiumDetail=None,
                        EtdDetail=None,
                    )
                    if options.has_content
                    else None
                ),
                ExpressFreightDetail=None,
                FreightShipmentDetail=None,
                DeliveryInstructions=None,
                VariableHandlingChargeDetail=None,
                CustomsClearanceDetail=(
                    CustomsClearanceDetail(
                        Brokers=None,
                        ClearanceBrokerage=None,
                        CustomsOptions=None,
                        ImporterOfRecord=None,
                        RecipientCustomsId=None,
                        DutiesPayment=(
                            Payment(
                                PaymentType=PaymentType[duty.paid_by or "sender"].value,
                                Payor=(
                                    Payor(
                                        ResponsibleParty=Party(
                                            AccountNumber=duty.account_number,
                                            Tins=bill_to.taxes,
                                        )
                                    )
                                    if any([duty.account_number, bill_to.taxes])
                                    else None
                                ),
                            )
                        ),
                        DocumentContent=None,
                        CustomsValue=(
                            Money(
                                Currency=(
                                    getattr(duty, "currency", options.currency) or "USD"
                                ),
                                Amount=(
                                    getattr(
                                        duty, "declared_value", options.declared_value
                                    )
                                    or 0.0
                                ),
                            )
                        ),
                        FreightOnValue=None,
                        InsuranceCharges=None,
                        PartiesToTransactionAreRelated=None,
                        CommercialInvoice=(
                            CommercialInvoice(
                                Comments=None,
                                FreightCharge=None,
                                TaxesOrMiscellaneousChargeType=None,
                                PackingCosts=None,
                                HandlingCosts=None,
                                SpecialInstructions=None,
                                DeclarationStatement=None,
                                PaymentTerms=None,
                                Purpose=PurposeType[
                                    customs.content_type or "other"
                                ].value,
                                PurposeOfShipmentDescription=None,
                                CustomerReferences=None,
                                OriginatorName=(
                                    shipper.company_name or shipper.person_name
                                ),
                                TermsOfSale=Incoterm[customs.incoterm or "DDU"].value,
                            )
                            if customs.commercial_invoice
                            else None
                        ),
                        Commodities=[
                            Commodity(
                                Name=None,
                                NumberOfPieces=item.quantity,
                                Description=item.description or "N/A",
                                Purpose=None,
                                CountryOfManufacture=(
                                    item.origin_country or shipper.country_code
                                ),
                                HarmonizedCode=None,
                                Weight=FedexWeight(
                                    Units=package.weight_unit.value,
                                    Value=Weight(item.weight, item.weight_unit)[
                                        package.weight_unit.value
                                    ],
                                ),
                                Quantity=item.quantity,
                                QuantityUnits="EA",
                                AdditionalMeasures=None,
                                UnitPrice=Money(
                                    Currency=(options.currency or duty.currency),
                                    Amount=item.value_amount,
                                ),
                                CustomsValue=None,
                                ExciseConditions=None,
                                ExportLicenseNumber=None,
                                ExportLicenseExpirationDate=None,
                                CIMarksAndNumbers=None,
                                PartNumber=item.sku,
                                NaftaDetail=None,
                            )
                            for item in customs.commodities
                        ],
                        ExportDetail=None,
                        RegulatoryControls=None,
                        DeclarationStatementDetail=None,
                    )
                    if payload.customs is not None
                    else None
                ),
                PickupDetail=None,
                SmartPostDetail=None,
                BlockInsightVisibility=None,
                LabelSpecification=LabelSpecification(
                    Dispositions=None,
                    LabelFormatType=LabelFormatType.COMMON_2_D.value,
                    ImageType=label_type,
                    LabelStockType=label_format,
                    LabelPrintingOrientation=LabelPrintingOrientationType.TOP_EDGE_OF_TEXT_FIRST.value,
                    LabelOrder=LabelOrderType.SHIPPING_LABEL_FIRST.value,
                    PrintedLabelOrigin=None,
                    CustomerSpecifiedDetail=None,
                ),
                ShippingDocumentSpecification=ShippingDocumentSpecification(
                    ShippingDocumentTypes=["COMMERCIAL_INVOICE"],
                    NotificationContentSpecification=None,
                    CertificateOfOrigin=None,
                    CommercialInvoiceDetail=CommercialInvoiceDetail(
                        Format=ShippingDocumentFormat(
                            Dispositions=None,
                            TopOfPageOffset=None,
                            ImageType="PDF",
                            StockType="PAPER_LETTER",
                            ProvideInstructions=None,
                            OptionsRequested=None,
                            Localization=None,
                            CustomDocumentIdentifier=None,
                        ),
                        CustomerImageUsages=None,
                        FormVersion=None,
                    ),
                    CustomPackageDocumentDetail=None,
                    CustomShipmentDocumentDetail=None,
                    ExportDeclarationDetail=None,
                    GeneralAgencyAgreementDetail=None,
                    NaftaCertificateOfOriginDetail=None,
                    DangerousGoodsShippersDeclarationDetail=None,
                    FreightAddressLabelDetail=None,
                    FreightBillOfLadingDetail=None,
                    ReturnInstructionsDetail=None,
                ),
                RateRequestTypes=None,
                EdtRequestType=None,
                MasterTrackingId=(
                    TrackingId(
                        TrackingIdType="[MASTER_ID_TYPE]",
                        TrackingNumber="[MASTER_TRACKING_ID]",
                    )
                    if package_index > 1
                    else None
                ),
                PackageCount=len(packages),
                ConfigurationData=None,
                RequestedPackageLineItems=[
                    RequestedPackageLineItem(
                        SequenceNumber=package_index,
                        GroupNumber=None,
                        GroupPackageCount=None,
                        VariableHandlingChargeDetail=None,
                        InsuredValue=None,
                        Weight=(
                            FedexWeight(
                                Units=package.weight.unit,
                                Value=package.weight.value,
                            )
                            if package.weight.value
                            else None
                        ),
                        Dimensions=(
                            FedexDimensions(
                                Length=package.length.map(MeasurementOptions).value,
                                Width=package.width.map(MeasurementOptions).value,
                                Height=package.height.map(MeasurementOptions).value,
                                Units=package.dimension_unit.value,
                            )
                            if (
                                # only set dimensions if the packaging type is set to your_packaging
                                package.has_dimensions
                                and PackagingType.map(
                                    package.packaging_type or "your_packaging"
                                ).value
                                == PackagingType.your_packaging.value
                            )
                            else None
                        ),
                        PhysicalPackaging=None,
                        ItemDescription=package.parcel.description,
                        ItemDescriptionForClearance=None,
                        CustomerReferences=(
                            [
                                CustomerReference(
                                    CustomerReferenceType=CustomerReferenceType.CUSTOMER_REFERENCE,
                                    Value=payload.reference,
                                )
                            ]
                            if any(payload.reference or "")
                            else None
                        ),
                        SpecialServicesRequested=None,
                        ContentRecords=None,
                    )
                ],
            ),
        )
        for package_index, package in enumerate(packages, 1)
    ]

    return Serializable(requests, _request_serializer)


def _request_serializer(requests: List[ProcessShipmentRequest]) -> List[str]:
    namespacedef_ = 'xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v26="http://fedex.com/ws/ship/v26"'

    def serialize(request: ProcessShipmentRequest):
        envelope = create_envelope(body_content=request)
        envelope.Body.ns_prefix_ = envelope.ns_prefix_
        apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "v26")

        return XP.export(envelope, namespacedef_=namespacedef_)

    return [serialize(request) for request in requests]
