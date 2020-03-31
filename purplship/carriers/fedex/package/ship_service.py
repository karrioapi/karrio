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
    Payor
)
from purplship.core.utils.helpers import export, concat_str
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.soap import clean_namespaces, create_envelope
from purplship.core.utils.xml import Element
from purplship.core.errors import RequiredFieldError
from purplship.core.units import Weight, Dimension, Options, Package
from purplship.core.models import ShipmentDetails, Message, ShipmentRequest
from purplship.carriers.fedex.error import parse_error_response
from purplship.carriers.fedex.utils import Settings
from purplship.carriers.fedex.units import PackagingType, ServiceType, SpecialServiceType, PackagePresets


NOTIFICATION_EVENTS = ['ON_DELIVERY', 'ON_ESTIMATED_DELIVERY', 'ON_EXCEPTION', 'ON_SHIPMENT', 'ON_TENDER']


def parse_shipment_response(
    response: Element, settings: Settings
) -> Tuple[ShipmentDetails, List[Message]]:
    detail = next(iter(response.xpath(".//*[local-name() = $name]", name="CompletedShipmentDetail")), None)
    shipment: ShipmentDetails = _extract_shipment(detail, settings) if detail is not None else None
    return shipment, parse_error_response(response, settings)


def _extract_shipment(
    shipment_detail_node: Element, settings: Settings
) -> ShipmentDetails:
    detail = CompletedShipmentDetail()
    detail.build(shipment_detail_node)

    tracking_number = cast(TrackingId, detail.MasterTrackingId).TrackingNumber
    package: CompletedPackageDetail = next(iter(detail.CompletedPackageDetails), None)
    part: ShippingDocumentPart = next(iter(package.Label.Parts)) if package is not None else None
    label = encodebytes(cast(ShippingDocumentPart, part).Image).decode('utf-8') if part is not None else None

    return ShipmentDetails(
        carrier=settings.carrier,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        label=label,
    )


def process_shipment_request(
    payload: ShipmentRequest, settings: Settings
) -> Serializable[ProcessShipmentRequest]:
    parcel_preset = PackagePresets[payload.parcel.package_preset].value if payload.parcel.package_preset else None
    package = Package(payload.parcel, parcel_preset)

    if package.weight.value is None:
        raise RequiredFieldError("parcel.weight")

    service = ServiceType[payload.service].value
    options = Options(payload.options)
    special_services = [
        SpecialServiceType[name].value
        for name, value in payload.options.items()
        if name in SpecialServiceType.__members__
    ]

    request = ProcessShipmentRequest(
        WebAuthenticationDetail=settings.webAuthenticationDetail,
        ClientDetail=settings.clientDetail,
        TransactionDetail=TransactionDetail(CustomerTransactionId="IE_v18_Ship"),
        Version=VersionId(ServiceId="ship", Major=25, Intermediate=0, Minor=0),
        RequestedShipment=RequestedShipment(
            ShipTimestamp=datetime.now(),
            DropoffType="REGULAR_PICKUP",
            ServiceType=service,
            PackagingType=PackagingType[payload.parcel.packaging_type or "small_box"].value,
            ManifestDetail=None,
            TotalWeight=FedexWeight(
                Units=package.weight_unit.value,
                Value=package.weight.value,
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
                PaymentType=None,
                Payor=Payor(
                    ResponsibleParty=Party(
                        AccountNumber=payload.payment.account_number,
                        Tins=None,
                        Contact=None,
                        Address=None
                    )
                ),
            ),
            SpecialServicesRequested=ShipmentSpecialServicesRequested(
                SpecialServiceTypes=special_services,
                CodDetail=CodDetail(
                    CodCollectionAmount=Money(
                        Currency=options.currency or "USD",
                        Amount=options.cash_on_delivery.amount
                    ),
                    AddTransportationChargesDetail=None,
                    CollectionType=CodCollectionType.CASH,
                    CodRecipient=None,
                    FinancialInstitutionContactAndAddress=None,
                    RemitToName=None,
                    ReferenceIndicator=None,
                    ReturnTrackingId=None
                ) if options.cash_on_delivery else None,
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
                                    EmailAddress=options.notification.email or payload.shipper.email,
                                    Name=payload.shipper.person_name
                                ),
                                Localization=Localization(
                                    LanguageCode="EN",
                                    LocaleCode=None
                                )
                            ),
                            FormatSpecification='TEXT'
                        )
                    ]
                ) if options.notification else None,
                ReturnShipmentDetail=None,
                PendingShipmentDetail=None,
                InternationalControlledExportDetail=None,
                InternationalTrafficInArmsRegulationsDetail=None,
                ShipmentDryIceDetail=None,
                HomeDeliveryPremiumDetail=None,
                EtdDetail=None,
                CustomDeliveryWindowDetail=None
            ) if options.has_content else None,
            ExpressFreightDetail=None,
            FreightShipmentDetail=None,
            DeliveryInstructions=None,
            VariableHandlingChargeDetail=None,
            CustomsClearanceDetail=None,
            PickupDetail=None,
            SmartPostDetail=None,
            BlockInsightVisibility=None,
            LabelSpecification=None,
            ShippingDocumentSpecification=None,
            RateRequestTypes=(
                ["LIST"] + ([] if options.currency is None else ["PREFERRED"])
            ),
            EdtRequestType=None,
            MasterTrackingId=None,
            PackageCount=None,
            ConfigurationData=None,
            RequestedPackageLineItems=[
                RequestedPackageLineItem(
                    SequenceNumber=index,
                    GroupNumber=None,
                    GroupPackageCount=index,
                    VariableHandlingChargeDetail=None,
                    InsuredValue=None,
                    Weight=FedexWeight(
                        Units=package.weight_unit.value,
                        Value=Weight(pkg.weight, package.weight_unit).value,
                    ) if pkg.weight else None,
                    Dimensions=FedexDimensions(
                        Length=Dimension(pkg.length, package.dimension_unit).value,
                        Width=Dimension(pkg.width, package.dimension_unit).value,
                        Height=Dimension(pkg.height, package.dimension_unit).value,
                        Units=package.dimension_unit.value,
                    ) if any([pkg.length, pkg.width, pkg.height]) else None,
                    PhysicalPackaging=None,
                    ItemDescription=pkg.description,
                    ItemDescriptionForClearance=None,
                    CustomerReferences=None,
                    SpecialServicesRequested=None,
                    ContentRecords=None,
                )
                for index, pkg in enumerate(payload.customs.commodities, 1)
            ]
            if payload.customs is not None
            else None,
        ),
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: ProcessShipmentRequest) -> str:
    return clean_namespaces(
        export(
            create_envelope(body_content=request),
            namespacedef_='tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://fedex.com/ws/ship/v25"',
        ),
        envelope_prefix="tns:",
        body_child_prefix="ns:",
        body_child_name="ProcessShipmentRequest",
    )
