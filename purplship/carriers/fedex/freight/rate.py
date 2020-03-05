from functools import reduce
from datetime import datetime
from typing import Tuple, List, Optional
from pyfedex.rate_service_v26 import (
    RateReplyDetail, RateRequest as FedexRateRequest, TransactionDetail, VersionId,
    RequestedShipment, Money, TaxpayerIdentification, Party, Contact, Address, Payment,
    Payor, ShipmentSpecialServicesRequested, FreightShipmentDetail,
    LabelSpecification, RequestedPackageLineItem,
    Weight, Dimensions, RatedShipmentDetail,
)
from purplship.core.utils.helpers import export
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.soap import clean_namespaces, create_envelope
from purplship.core.units import Currency
from purplship.core.utils.xml import Element
from purplship.core.models import (
    RateDetails, RateRequest, Error, ChargeDetails
)
from purplship.carriers.fedex.units import PackagingType, ServiceType, PaymentType, SpecialServiceType
from purplship.carriers.fedex.error import parse_error_response
from purplship.carriers.fedex.utils import Settings


def parse_rate_response(response: Element, settings: Settings) -> Tuple[List[RateDetails], List[Error]]:
    rate_reply = response.xpath(".//*[local-name() = $name]", name="RateReplyDetails")
    rate_details: List[RateDetails] = [_extract_quote(detail_node, settings) for detail_node in rate_reply]
    return (
        [details for details in rate_details if details is not None],
        parse_error_response(response, settings)
    )


def _extract_quote(detail_node: Element, settings: Settings) -> Optional[RateDetails]:
    detail = RateReplyDetail()
    detail.build(detail_node)
    if not detail.RatedShipmentDetails:
        return None
    shipmentDetail: RatedShipmentDetail = detail.RatedShipmentDetails[0].ShipmentRateDetail
    delivery_ = reduce(
        lambda v, c: c.text, detail_node.xpath(".//*[local-name() = $name]", name="DeliveryTimestamp"), None
    )
    currency_ = reduce(
        lambda v, c: c.text, detail_node.xpath(".//*[local-name() = $name]", name="Currency"),
        Currency.USD.name
    )
    Discounts_ = map(
        lambda d: ChargeDetails(
            name=d.RateDiscountType, amount=float(d.Amount.Amount), currency=currency_
        ),
        shipmentDetail.FreightDiscounts,
    )
    Surcharges_ = map(
        lambda s: ChargeDetails(
            name=s.SurchargeType, amount=float(s.Amount.Amount), currency=currency_
        ),
        shipmentDetail.Surcharges,
    )
    Taxes_ = map(
        lambda t: ChargeDetails(name=t.TaxType, amount=float(t.Amount.Amount), currency=currency_),
        shipmentDetail.Taxes,
    )
    return RateDetails(
        carrier=settings.carrier_name,
        service_name=detail.ServiceType,
        service_type=detail.ActualRateType,
        currency=currency_,
        delivery_date=(
            datetime.strptime(delivery_, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d") if delivery_ else None
        ),
        base_charge=float(shipmentDetail.TotalBaseCharge.Amount),
        total_charge=float(shipmentDetail.TotalNetChargeWithDutiesAndTaxes.Amount),
        duties_and_taxes=float(shipmentDetail.TotalTaxes.Amount),
        discount=float(shipmentDetail.TotalFreightDiscounts.Amount),
        extra_charges=list(Discounts_) + list(Surcharges_) + list(Taxes_),
    )


def rate_request(payload: RateRequest, settings: Settings) -> Serializable[FedexRateRequest]:
    requested_services = [svc for svc in payload.shipment.services if svc in ServiceType.__members__]
    options = [opt for opt in payload.shipment.options.keys() if opt.code in SpecialServiceType.__members__]

    request = FedexRateRequest(
        WebAuthenticationDetail=settings.webAuthenticationDetail,
        ClientDetail=settings.clientDetail,
        TransactionDetail=TransactionDetail(CustomerTransactionId="FTC"),
        Version=VersionId(ServiceId="crs", Major=22, Intermediate=0, Minor=0),
        ReturnTransitAndCommit=True,
        CarrierCodes=None,
        VariableOptions=None,
        ConsolidationKey=None,
        RequestedShipment=RequestedShipment(
            ShipTimestamp=datetime.now(),
            DropoffType=None,
            ServiceType=(
                ServiceType[requested_services[0]].value if len(requested_services) > 0 else None
            ),
            PackagingType=PackagingType[payload.shipment.packaging_type or "YOUR_PACKAGING"].value,
            VariationOptions=None,
            TotalWeight=Weight(
                Units=payload.shipment.weight_unit,
                Value=payload.shipment.total_weight
                or reduce(lambda r, p: r + p.weight, payload.shipment.items, 0.0),
            ),
            TotalInsuredValue=(
                Money(
                    Currency=payload.shipment.currency,
                    Amount=payload.shipment.insured_amount,
                )
                if payload.shipment.insured_amount is not None else None
            ),
            PreferredCurrency=payload.shipment.currency,
            ShipmentAuthorizationDetail=None,
            Shipper=Party(
                AccountNumber=payload.shipper.account_number,
                Tins=(
                    [
                        TaxpayerIdentification(
                            TinType=None,
                            Usage=None,
                            Number=payload.shipper.tax_id,
                            EffectiveDate=None,
                            ExpirationDate=None,
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
                    EMailAddress=None,
                )
                if any(
                    (
                        payload.shipper.company_name,
                        payload.shipper.person_name,
                        payload.shipper.phone_number,
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
                AccountNumber=payload.recipient.account_number,
                Tins=(
                    [
                        TaxpayerIdentification(
                            TinType=None,
                            Usage=None,
                            Number=payload.recipient.tax_id,
                            EffectiveDate=None,
                            ExpirationDate=None,
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
                        payload.recipient.person_name,
                        payload.recipient.phone_number,
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
                    Payor(
                        ResponsibleParty=Party(
                            AccountNumber=payload.shipment.payment_account_number,
                            Tins=None,
                            Contact=None,
                            Address=None,
                        )
                    )
                    if payload.shipment.payment_account_number is not None
                    else None
                ),
            )
            if any(
                (payload.shipment.paid_by, payload.shipment.payment_account_number)
            )
            else None,
            SpecialServicesRequested=ShipmentSpecialServicesRequested(
                SpecialServiceTypes=[
                    SpecialServiceType[option].value for option in options
                ],
                CodDetail=None,
                DeliveryOnInvoiceAcceptanceDetail=None,
                HoldAtLocationDetail=None,
                EventNotificationDetail=None,
                ReturnShipmentDetail=None,
                PendingShipmentDetail=None,
                InternationalControlledExportDetail=None,
                InternationalTrafficInArmsRegulationsDetail=None,
                ShipmentDryIceDetail=None,
                HomeDeliveryPremiumDetail=None,
                FlatbedTrailerDetail=None,
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
                HazardousMaterialsOfferor=None,
                LineItems=None,
            )
            if any([svc for svc in requested_services if "FREIGHT" in svc])
            else None,
            DeliveryInstructions=None,
            VariableHandlingChargeDetail=None,
            CustomsClearanceDetail=None,
            PickupDetail=None,
            SmartPostDetail=None,
            BlockInsightVisibility=None,
            LabelSpecification=LabelSpecification(
                LabelFormatType=payload.shipment.label.format,
                ImageType=payload.shipment.label.type,
                LabelStockType=None,
                LabelPrintingOrientation=None,
                LabelOrder=None,
                PrintedLabelOrigin=None,
                CustomerSpecifiedDetail=None,
            )
            if payload.shipment.label is not None
            else None,
            ShippingDocumentSpecification=None,
            RateRequestTypes=(
                ["LIST"] + ([] if not payload.shipment.currency else ["PREFERRED"])
            ),
            EdtRequestType=None,
            PackageCount=len(payload.shipment.items),
            ShipmentOnlyFields=None,
            ConfigurationData=None,
            RequestedPackageLineItems=[
                RequestedPackageLineItem(
                    SequenceNumber=None,
                    GroupNumber=None,
                    GroupPackageCount=index + 1,
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
                    ItemDescription=pkg.content,
                    ItemDescriptionForClearance=pkg.description,
                    CustomerReferences=None,
                    SpecialServicesRequested=None,
                    ContentRecords=None,
                )
                for index, pkg in enumerate(payload.shipment.items)
            ],
        ),
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: FedexRateRequest) -> str:
    return clean_namespaces(
        export(
            create_envelope(body_content=request),
            namespacedef_='xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:ns="http://fedex.com/ws/rate/v22"',
        ),
        envelope_prefix="tns:",
        body_child_prefix="ns:",
        body_child_name="RateRequest",
    )
