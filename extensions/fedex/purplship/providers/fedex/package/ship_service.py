from datetime import datetime
from base64 import encodebytes
from typing import List, Tuple, cast
from pyfedex.ship_service_v25 import (
    CompletedShipmentDetail,
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
    CompletedPackageDetail,
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
    ShippingDocumentPart,
    Payment,
    Payor,
    WeightUnits,
    LabelSpecification,
    LabelFormatType,
    LabelStockType,
    ShippingDocumentImageType,
    LabelPrintingOrientationType,
)
from purplship.core.utils.helpers import export, concat_str
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.soap import apply_namespaceprefix, create_envelope
from purplship.core.utils.xml import Element
from purplship.core.units import Weight, Dimension, Options, Packages
from purplship.core.models import ShipmentDetails, Message, ShipmentRequest
from purplship.providers.fedex.error import parse_error_response
from purplship.providers.fedex.utils import Settings
from purplship.providers.fedex.units import (
    PackagingType,
    ServiceType,
    SpecialServiceType,
    PackagePresets,
    PaymentType,
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
    detail = next(
        iter(
            response.xpath(".//*[local-name() = $name]", name="CompletedShipmentDetail")
        ),
        None,
    )
    shipment: ShipmentDetails = (
        _extract_shipment(detail, settings) if detail is not None else None
    )
    return shipment, parse_error_response(response, settings)


def _extract_shipment(
    shipment_detail_node: Element, settings: Settings
) -> ShipmentDetails:
    detail = CompletedShipmentDetail()
    detail.build(shipment_detail_node)

    tracking_number = cast(TrackingId, detail.MasterTrackingId).TrackingNumber
    package: CompletedPackageDetail = next(iter(detail.CompletedPackageDetails), None)
    part: ShippingDocumentPart = (
        next(iter(package.Label.Parts)) if package is not None else None
    )
    label = (
        encodebytes(cast(ShippingDocumentPart, part).Image).decode("utf-8")
        if part is not None
        else None
    )

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=tracking_number,
        shipment_identifier=tracking_number,
        label=label,
    )


def process_shipment_request(
    payload: ShipmentRequest, settings: Settings
) -> Serializable[ProcessShipmentRequest]:
    packages = Packages(payload.parcels, PackagePresets, required=["weight"])
    # Only the master package is selected here because even for MPS only one package is accepted for a master tracking.
    master_package = packages[0]
    package_type = (
        PackagingType[master_package.packaging_type or "your_packaging"].value
        if len(packages) == 1
        else PackagingType.your_packaging.value
    )

    service = ServiceType[payload.service].value
    options = Options(payload.options)
    special_services = [
        SpecialServiceType[name].value
        for name, value in payload.options.items()
        if name in SpecialServiceType.__members__
    ]
    payment_type = PaymentType[payload.payment.paid_by or "sender"].value

    request = ProcessShipmentRequest(
        WebAuthenticationDetail=settings.webAuthenticationDetail,
        ClientDetail=settings.clientDetail,
        TransactionDetail=TransactionDetail(CustomerTransactionId="IE_v25_Ship"),
        Version=VersionId(ServiceId="ship", Major=25, Intermediate=0, Minor=0),
        RequestedShipment=RequestedShipment(
            ShipTimestamp=datetime.now(),
            DropoffType="REGULAR_PICKUP",
            ServiceType=service,
            PackagingType=package_type,
            ManifestDetail=None,
            TotalWeight=FedexWeight(
                Units=WeightUnits.LB.value, Value=packages.weight.LB
            ),
            TotalInsuredValue=options.insurance.amount if options.insurance else None,
            PreferredCurrency=options.currency,
            ShipmentAuthorizationDetail=None,
            Shipper=Party(
                AccountNumber=settings.account_number,
                Tins=[
                    TaxpayerIdentification(TinType=None, Number=tax)
                    for tax in [
                        payload.shipper.federal_tax_id,
                        payload.shipper.state_tax_id,
                    ]
                ]
                if any([payload.shipper.federal_tax_id, payload.shipper.state_tax_id])
                else None,
                Contact=Contact(
                    ContactId=None,
                    PersonName=payload.shipper.person_name,
                    Title=None,
                    CompanyName=payload.shipper.company_name,
                    PhoneNumber=payload.shipper.phone_number,
                    PhoneExtension=None,
                    TollFreePhoneNumber=None,
                    PagerNumber=None,
                    FaxNumber=None,
                    EMailAddress=payload.shipper.email,
                )
                if any(
                    (
                        payload.shipper.company_name,
                        payload.shipper.phone_number,
                        payload.shipper.person_name,
                        payload.shipper.email,
                    )
                )
                else None,
                Address=Address(
                    StreetLines=concat_str(
                        payload.shipper.address_line1, payload.shipper.address_line2
                    ),
                    City=payload.shipper.city,
                    StateOrProvinceCode=payload.shipper.state_code,
                    PostalCode=payload.shipper.postal_code,
                    UrbanizationCode=None,
                    CountryCode=payload.shipper.country_code,
                    CountryName=None,
                    Residential=None,
                    GeographicCoordinates=None,
                ),
            ),
            Recipient=Party(
                AccountNumber=None,
                Tins=[
                    TaxpayerIdentification(TinType=None, Number=tax)
                    for tax in [
                        payload.recipient.federal_tax_id,
                        payload.recipient.state_tax_id,
                    ]
                ]
                if any(
                    [payload.recipient.federal_tax_id, payload.recipient.state_tax_id]
                )
                else None,
                Contact=Contact(
                    ContactId=None,
                    PersonName=payload.recipient.person_name,
                    Title=None,
                    CompanyName=payload.recipient.company_name,
                    PhoneNumber=payload.recipient.phone_number,
                    PhoneExtension=None,
                    TollFreePhoneNumber=None,
                    PagerNumber=None,
                    FaxNumber=None,
                    EMailAddress=payload.recipient.email,
                )
                if any(
                    (
                        payload.recipient.company_name,
                        payload.recipient.phone_number,
                        payload.recipient.person_name,
                        payload.recipient.email,
                    )
                )
                else None,
                Address=Address(
                    StreetLines=concat_str(
                        payload.recipient.address_line1,
                        payload.recipient.address_line2,
                    ),
                    City=payload.recipient.city,
                    StateOrProvinceCode=payload.recipient.state_code,
                    PostalCode=payload.recipient.postal_code,
                    UrbanizationCode=None,
                    CountryCode=payload.recipient.country_code,
                    CountryName=None,
                    Residential=None,
                    GeographicCoordinates=None,
                ),
            ),
            RecipientLocationNumber=None,
            Origin=None,
            SoldTo=None,
            ShippingChargesPayment=Payment(
                PaymentType=payment_type,
                Payor=Payor(
                    ResponsibleParty=Party(
                        AccountNumber=payload.payment.account_number
                        or settings.account_number,
                        Tins=None,
                        Contact=None,
                        Address=None,
                    )
                ),
            ),
            SpecialServicesRequested=ShipmentSpecialServicesRequested(
                SpecialServiceTypes=special_services,
                CodDetail=CodDetail(
                    CodCollectionAmount=Money(
                        Currency=options.currency or "USD",
                        Amount=options.cash_on_delivery.amount,
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
                else None,
                DeliveryOnInvoiceAcceptanceDetail=None,
                HoldAtLocationDetail=None,
                EventNotificationDetail=ShipmentEventNotificationDetail(
                    AggregationType=None,
                    PersonalMessage=None,
                    EventNotifications=[
                        ShipmentEventNotificationSpecification(
                            Role=None,
                            Events=NOTIFICATION_EVENTS,
                            NotificationDetail=NotificationDetail(
                                NotificationType="EMAIL",
                                EmailDetail=EMailDetail(
                                    EmailAddress=options.notification.email
                                    or payload.shipper.email,
                                    Name=payload.shipper.person_name,
                                ),
                                Localization=Localization(
                                    LanguageCode="EN", LocaleCode=None
                                ),
                            ),
                            FormatSpecification="TEXT",
                        )
                    ],
                )
                if options.notification
                else None,
                ReturnShipmentDetail=None,
                PendingShipmentDetail=None,
                InternationalControlledExportDetail=None,
                InternationalTrafficInArmsRegulationsDetail=None,
                ShipmentDryIceDetail=None,
                HomeDeliveryPremiumDetail=None,
                EtdDetail=None,
                CustomDeliveryWindowDetail=None,
            )
            if options.has_content
            else None,
            ExpressFreightDetail=None,
            FreightShipmentDetail=None,
            DeliveryInstructions=None,
            VariableHandlingChargeDetail=None,
            CustomsClearanceDetail=None,
            PickupDetail=None,
            SmartPostDetail=None,
            BlockInsightVisibility=None,
            LabelSpecification=LabelSpecification(
                Dispositions=None,
                LabelFormatType=LabelFormatType.COMMON_2_D.value,
                ImageType=ShippingDocumentImageType.PDF.value,
                LabelStockType=LabelStockType.PAPER__7_X_4_75.value,
                LabelPrintingOrientation=LabelPrintingOrientationType.TOP_EDGE_OF_TEXT_FIRST.value,
                LabelOrder=None,
                PrintedLabelOrigin=None,
                CustomerSpecifiedDetail=None,
            ),
            ShippingDocumentSpecification=None,
            RateRequestTypes=None,
            EdtRequestType=None,
            MasterTrackingId=None,
            PackageCount=len(packages),
            ConfigurationData=None,
            RequestedPackageLineItems=[
                RequestedPackageLineItem(
                    SequenceNumber=1,
                    GroupNumber=None,
                    GroupPackageCount=None,
                    VariableHandlingChargeDetail=None,
                    InsuredValue=None,
                    Weight=FedexWeight(
                        Units=master_package.weight_unit.value,
                        Value=master_package.weight.value,
                    )
                    if master_package.weight.value
                    else None,
                    Dimensions=FedexDimensions(
                        Length=master_package.length.value,
                        Width=master_package.width.value,
                        Height=master_package.height.value,
                        Units=master_package.dimension_unit.value,
                    )
                    if any(
                        [
                            master_package.length,
                            master_package.width,
                            master_package.height,
                        ]
                    )
                    else None,
                    PhysicalPackaging=None,
                    ItemDescription=master_package.parcel.description,
                    ItemDescriptionForClearance=None,
                    CustomerReferences=None,
                    SpecialServicesRequested=None,
                    ContentRecords=None,
                )
            ],
        ),
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: ProcessShipmentRequest) -> str:
    namespacedef_ = 'xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v25="http://fedex.com/ws/ship/v25"'

    envelope = create_envelope(body_content=request)
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "v25")

    return export(envelope, namespacedef_=namespacedef_)
