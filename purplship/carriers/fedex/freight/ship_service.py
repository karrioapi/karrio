from base64 import b64encode
from datetime import datetime
from typing import List, Tuple
from functools import reduce
from pyfedex.ship_service_v21 import (
    CompletedShipmentDetail, ShipmentRateDetail, CompletedPackageDetail, ProcessShipmentRequest,
    TransactionDetail, VersionId, RequestedShipment, RequestedPackageLineItem, Weight, Party,
    Contact, Address, TaxpayerIdentification, Payment, Payor, ShipmentSpecialServicesRequested,
    FreightShipmentDetail, SmartPostShipmentDetail, SmartPostShipmentProcessingOptionsRequested,
    LabelSpecification, Dimensions, CustomerReference, InternationalTrafficInArmsRegulationsDetail,
)
from purplship.core.utils.helpers import export
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.soap import clean_namespaces, create_envelope
from purplship.core.utils.xml import Element
from purplship.core.models import ShipmentDetails, Error, ChargeDetails, ShipmentRequest
from purplship.carriers.fedex.error import parse_error_response
from purplship.carriers.fedex.utils import Settings
from purplship.carriers.fedex.units import (
    PackagingType, ServiceType, PaymentType, SpecialServiceType,
)


def parse_shipment_response(response: Element, settings: Settings) -> Tuple[ShipmentDetails, List[Error]]:
    details = response.xpath(".//*[local-name() = $name]", name="CompletedShipmentDetail")
    shipment: ShipmentDetails = _extract_shipment(details[0], settings) if len(details) > 0 else None
    return shipment, parse_error_response(response, settings)


def _extract_shipment(shipment_detail_node: Element, settings: Settings) -> ShipmentDetails:
    detail = CompletedShipmentDetail()
    detail.build(shipment_detail_node)

    shipment: ShipmentRateDetail = detail.ShipmentRating.ShipmentRateDetails[0]
    items: CompletedPackageDetail = detail.CompletedPackageDetails

    return ShipmentDetails(
        carrier=settings.carrier_name,
        tracking_numbers=reduce(
            lambda ids, pkg: ids + [_id.TrackingNumber for _id in pkg.TrackingIds],
            items, [],
        ),
        total_charge=ChargeDetails(
            name="Shipment charge",
            amount=shipment.TotalNetChargeWithDutiesAndTaxes.Amount,
            currency=shipment.TotalNetChargeWithDutiesAndTaxes.Currency,
        ),
        charges=[
            ChargeDetails(
                name="base_charge",
                amount=shipment.TotalBaseCharge.Amount,
                currency=shipment.TotalBaseCharge.Currency,
            ),
            ChargeDetails(
                name="discount",
                amount=detail.ShipmentRating.EffectiveNetDiscount.Amount,
                currency=detail.ShipmentRating.EffectiveNetDiscount.Currency,
            ),
        ]
        + [
            ChargeDetails(
                name=surcharge.SurchargeType,
                amount=surcharge.Amount.Amount,
                currency=surcharge.Amount.Currency,
            )
            for surcharge in shipment.Surcharges
        ]
        + [
            ChargeDetails(
                name=fee.Type,
                amount=fee.Amount.Amount,
                currency=fee.Amount.Currency,
            )
            for fee in shipment.AncillaryFeesAndTaxes
        ],
        services=[detail.ServiceTypeDescription],
        documents=reduce(
            lambda labels, pkg: labels + [str(b64encode(part.Image), "utf-8") for part in pkg.Label.Parts],
            items, [],
        ),
    )


def process_shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable[ProcessShipmentRequest]:
    requested_services = [
        svc for svc in payload.shipment.services if svc in ServiceType.__members__
    ]
    options = [
        opt for opt in payload.shipment.options if opt.code in SpecialServiceType.__members__
    ]
    request = ProcessShipmentRequest(
        WebAuthenticationDetail=settings.webAuthenticationDetail,
        ClientDetail=settings.clientDetail,
        TransactionDetail=TransactionDetail(CustomerTransactionId="IE_v18_Ship"),
        Version=VersionId(ServiceId="ship", Major=21, Intermediate=0, Minor=0),
        RequestedShipment=RequestedShipment(
            ShipTimestamp=datetime.now(),
            DropoffType=payload.shipment.extra.get("DropoffType"),
            ServiceType=ServiceType[requested_services[0]].value
            if len(requested_services) > 0
            else None,
            PackagingType=PackagingType[
                payload.shipment.packaging_type or "YOUR_PACKAGING"
            ].value,
            ManifestDetail=None,
            TotalWeight=Weight(
                Units=payload.shipment.weight_unit,
                Value=payload.shipment.total_weight
                or reduce(lambda r, p: r + p.weight, payload.shipment.items, 0.0),
            ),
            TotalInsuredValue=payload.shipment.insured_amount,
            PreferredCurrency=payload.shipment.currency,
            ShipmentAuthorizationDetail=None,
            Shipper=Party(
                AccountNumber=payload.shipper.account_number,
                Tins=(
                    [
                        TaxpayerIdentification(
                            TinType=payload.shipper.extra.get("TinType"),
                            Usage=payload.shipper.extra.get("Usage"),
                            Number=payload.shipper.tax_id,
                            EffectiveDate=payload.shipper.extra.get("EffectiveDate"),
                            ExpirationDate=payload.shipper.extra.get("ExpirationDate"),
                        )
                    ]
                    if payload.shipper.tax_id is not None else None
                ),
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
                    EMailAddress=payload.shipper.email_address,
                )
                if any(
                    (
                        payload.shipper.company_name,
                        payload.shipper.phone_number,
                        payload.shipper.person_name,
                        payload.shipper.email_address,
                    )
                )
                else None,
                Address=Address(
                    StreetLines=payload.shipper.address_lines,
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
                AccountNumber=payload.recipient.extra.get("AccountNumber"),
                Tins=(
                    [
                        TaxpayerIdentification(
                            TinType=payload.recipient.extra.get("TinType"),
                            Usage=payload.recipient.extra.get("Usage"),
                            Number=payload.recipient.tax_id,
                            EffectiveDate=payload.recipient.extra.get("EffectiveDate"),
                            ExpirationDate=payload.recipient.extra.get(
                                "ExpirationDate"
                            ),
                        )
                    ]
                    if payload.recipient.tax_id is not None else None
                ),
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
                    EMailAddress=payload.recipient.email_address,
                )
                if any(
                    (
                        payload.recipient.company_name,
                        payload.recipient.phone_number,
                        payload.recipient.person_name,
                        payload.recipient.email_address,
                    )
                )
                else None,
                Address=Address(
                    StreetLines=payload.recipient.address_lines,
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
                PaymentType=PaymentType[payload.shipment.paid_by or "SENDER"].value,
                Payor=(
                    lambda payor: Payor(
                        ResponsibleParty=Party(
                            AccountNumber=payload.shipment.payment_account_number,
                            Tins=(
                                [
                                    TaxpayerIdentification(
                                        TinType=payor.extra.get("TinType"),
                                        Number=payor.tax_id,
                                        Usage=payor.extra.get("Usage"),
                                        EffectiveDate=payor.extra.get("EffectiveDate"),
                                        ExpirationDate=payor.extra.get(
                                            "ExpirationDate"
                                        ),
                                    )
                                ]
                                if payor.tax_id is not None else None
                            ),
                            Contact=Contact(
                                ContactId=payor.extra.get("ContactId"),
                                PersonName=payor.person_name,
                                Title=None,
                                CompanyName=payor.company_name,
                                PhoneNumber=payor.phone_number,
                                PhoneExtension=None,
                                TollFreePhoneNumber=None,
                                PagerNumber=None,
                                FaxNumber=None,
                                EMailAddress=payor.email_address,
                            )
                            if any(
                                (
                                    payor.company_name,
                                    payor.phone_number,
                                    payor.person_name,
                                    payor.email_address,
                                )
                            )
                            else None,
                            Address=Address(
                                StreetLines=payor.address_lines,
                                City=payor.city,
                                StateOrProvinceCode=payor.state_code,
                                PostalCode=payor.postal_code,
                                UrbanizationCode=None,
                                CountryCode=payor.country_code,
                                CountryName=None,
                                Residential=None,
                                GeographicCoordinates=None,
                            )
                            if any(
                                (
                                    payor.country_code,
                                    payor.address_lines,
                                    payor.city,
                                    payor.state_code,
                                    payor.postal_code,
                                )
                            )
                            else None,
                        )
                    )
                    if payload.shipment.payment_account_number is not None
                    else None
                )(
                    Party(
                        **payload.shipment.extra.get("Payor").get("ResponsibleParty")
                    )
                )
                if "Payor" in payload.shipment.extra
                else None,
            )
            if any(
                (payload.shipment.paid_by, payload.shipment.payment_account_number)
            )
            else None,
            SpecialServicesRequested=ShipmentSpecialServicesRequested(
                SpecialServiceTypes=[
                    SpecialServiceType[opt.code].value for opt in options
                ],
                CodDetail=None,
                DeliveryOnInvoiceAcceptanceDetail=None,
                HoldAtLocationDetail=None,
                EventNotificationDetail=None,
                ReturnShipmentDetail=None,
                PendingShipmentDetail=None,
                InternationalControlledExportDetail=None,
                InternationalTrafficInArmsRegulationsDetail=(
                    InternationalTrafficInArmsRegulationsDetail(
                        LicenseOrExemptionNumber=payload.shipment.extra.get(
                            "SpecialServicesRequested"
                        )
                        .get("InternationalTrafficInArmsRegulationsDetail")
                        .get("LicenseOrExemptionNumber")
                    )
                )
                if "SpecialServicesRequested" in payload.shipment.extra
                and "InternationalTrafficInArmsRegulationsDetail"
                in payload.shipment.extra.get("SpecialServicesRequested")
                else None,
                ShipmentDryIceDetail=None,
                HomeDeliveryPremiumDetail=None,
                FreightGuaranteeDetail=None,
                EtdDetail=None,
                CustomDeliveryWindowDetail=None,
            )
            if len(options) > 0
            else None,
            ExpressFreightDetail=None,
            FreightShipmentDetail=FreightShipmentDetail(
                FedExFreightAccountNumber=None,
                FedExFreightBillingContactAndAddress=None,
                AlternateBilling=None,
                PrintedReferences=None,
                Role=None,
                CollectTermsType=None,
                DeclaredValuePerUnit=None,
                DeclaredValueUnits=None,
                LiabilityCoverageDetail=None,
                Coupons=None,
                TotalHandlingUnits=None,
                ClientDiscountPercent=None,
                PalletWeight=None,
                ShipmentDimensions=None,
                Comment=None,
                SpecialServicePayments=None,
                HazardousMaterialsEmergencyContactNumber=None,
                HazardousMaterialsOfferor=None,
                LineItems=None,
            )
            if any([svc for svc in requested_services if "FREIGHT" in svc])
            else None,
            DeliveryInstructions=None,
            VariableHandlingChargeDetail=None,
            CustomsClearanceDetail=None,
            PickupDetail=None,
            SmartPostDetail=(
                lambda smart_post: SmartPostShipmentDetail(
                    ProcessingOptionsRequested=SmartPostShipmentProcessingOptionsRequested(
                        Options=smart_post.get("ProcessingOptionsRequested").get(
                            "Options"
                        )
                    )
                    if "ProcessingOptionsRequested" in smart_post
                    else None,
                    Indicia=smart_post.get("Indicia"),
                    AncillaryEndorsement=smart_post.get("AncillaryEndorsement"),
                    HubId=smart_post.get("HubId"),
                    CustomerManifestId=smart_post.get("CustomerManifestId"),
                )
            )(payload.shipment.extra.get("SmartPostDetail"))
            if "SmartPostDetail" in payload.shipment.extra
            else None,
            BlockInsightVisibility=None,
            LabelSpecification=LabelSpecification(
                Dispositions=payload.shipment.label.extra.get("Dispositions"),
                LabelFormatType=payload.shipment.label.format,
                ImageType=payload.shipment.label.type,
                LabelStockType=payload.shipment.label.extra.get("LabelStockType"),
                LabelPrintingOrientation=payload.shipment.label.extra.get(
                    "LabelPrintingOrientation"
                ),
                LabelOrder=payload.shipment.label.extra.get("LabelOrder"),
                PrintedLabelOrigin=payload.shipment.label.extra.get(
                    "PrintedLabelOrigin"
                ),
                CustomerSpecifiedDetail=None,
            )
            if payload.shipment.label is not None
            else None,
            ShippingDocumentSpecification=None,
            RateRequestTypes=(
                ["LIST"] + ([] if not payload.shipment.currency else ["PREFERRED"])
            ),
            EdtRequestType=payload.shipment.extra.get("EdtRequestType"),
            MasterTrackingId=None,
            PackageCount=len(payload.shipment.items),
            ConfigurationData=None,
            RequestedPackageLineItems=[
                RequestedPackageLineItem(
                    SequenceNumber=index + 1,
                    GroupNumber=None,
                    GroupPackageCount=None,
                    VariableHandlingChargeDetail=None,
                    InsuredValue=None,
                    Weight=Weight(
                        Units=payload.shipment.weight_unit, Value=pkg.weight
                    ),
                    Dimensions=Dimensions(
                        Length=pkg.length,
                        Width=pkg.width,
                        Height=pkg.height,
                        Units=payload.shipment.dimension_unit,
                    ),
                    PhysicalPackaging=None,
                    ItemDescription=pkg.description,
                    ItemDescriptionForClearance=pkg.content,
                    CustomerReferences=(
                        [
                            CustomerReference(
                                CustomerReferenceType=ref.get("CustomerReferenceType"),
                                Value=ref.get("Value"),
                            )
                            for ref in pkg.extra.get("CustomerReferences")
                        ]
                        if "CustomerReferences" in pkg.extra else None
                    ),
                    SpecialServicesRequested=None,
                    ContentRecords=None,
                )
                for index, pkg in enumerate(payload.shipment.items)
            ],
        ),
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: ProcessShipmentRequest) -> str:
    return clean_namespaces(
        export(
            create_envelope(body_content=request),
            namespacedef_='xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://fedex.com/ws/ship/v21"',
        ),
        envelope_prefix="tns:",
        body_child_prefix="ns:",
        body_child_name="ProcessShipmentRequest",
    )
