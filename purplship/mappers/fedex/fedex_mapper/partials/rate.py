from pyfedex.rate_v22 import (
    ClientDetail,
    RateReplyDetail,
    RateRequest,
    TransactionDetail,
    VersionId,
    RequestedShipment,
    Money,
    TaxpayerIdentification,
    Party,
    Contact,
    Address,
    Payment,
    Payor,
    ShipmentSpecialServicesRequested,
    FreightShipmentDetail,
    SmartPostShipmentDetail,
    SmartPostShipmentProcessingOptionsRequested,
    LabelSpecification,
    RequestedPackageLineItem,
    Weight,
    Dimensions,
)
from datetime import datetime
from lxml import etree
from .interface import reduce, Tuple, List, T, FedexMapperBase
from purplship.mappers.fedex.fedex_units import (
    PackagingType,
    ServiceType,
    PaymentType,
    SpecialServiceType,
)


class FedexMapperPartial(FedexMapperBase):
    def parse_rate_reply(
        self, response: etree.ElementBase
    ) -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        rate_replys = response.xpath(
            ".//*[local-name() = $name]", name="RateReplyDetails"
        )
        quotes: List[T.QuoteDetails] = reduce(self._extract_quote, rate_replys, [])
        return (quotes, self.parse_error_response(response))

    def _extract_quote(
        self, quotes: List[T.QuoteDetails], detailNode: etree.ElementBase
    ) -> List[T.QuoteDetails]:
        detail = RateReplyDetail()
        detail.build(detailNode)
        if not detail.RatedShipmentDetails:
            return quotes
        shipmentDetail = detail.RatedShipmentDetails[0].ShipmentRateDetail
        Discounts_ = map(
            lambda d: T.ChargeDetails(
                name=d.RateDiscountType, amount=float(d.Amount.Amount)
            ),
            shipmentDetail.FreightDiscounts,
        )
        Surcharges_ = map(
            lambda s: T.ChargeDetails(
                name=s.SurchargeType, amount=float(s.Amount.Amount)
            ),
            shipmentDetail.Surcharges,
        )
        Taxes_ = map(
            lambda t: T.ChargeDetails(name=t.TaxType, amount=float(t.Amount.Amount)),
            shipmentDetail.Taxes,
        )
        return quotes + [
            T.QuoteDetails(
                carrier=self.client.carrier_name,
                service_name=detail.ServiceType,
                service_type=detail.ActualRateType,
                currency=shipmentDetail.CurrencyExchangeRate.IntoCurrency
                if shipmentDetail.CurrencyExchangeRate
                else None,
                base_charge=float(shipmentDetail.TotalBaseCharge.Amount),
                total_charge=float(
                    shipmentDetail.TotalNetChargeWithDutiesAndTaxes.Amount
                ),
                duties_and_taxes=float(shipmentDetail.TotalTaxes.Amount),
                discount=float(shipmentDetail.TotalFreightDiscounts.Amount),
                extra_charges=list(Discounts_) + list(Surcharges_) + list(Taxes_),
            )
        ]

    def create_rate_request(self, payload: T.shipment_request) -> RateRequest:
        requested_services = [
            svc for svc in payload.shipment.services if svc in ServiceType.__members__
        ]
        options = [
            opt
            for opt in payload.shipment.options
            if opt.code in SpecialServiceType.__members__
        ]
        return RateRequest(
            WebAuthenticationDetail=self.webAuthenticationDetail,
            ClientDetail=ClientDetail(
                AccountNumber=payload.shipper.account_number, 
                MeterNumber=self.client.meter_number
            ),
            TransactionDetail=TransactionDetail(CustomerTransactionId="FTC"),
            Version=VersionId(ServiceId="crs", Major=22, Intermediate=0, Minor=0),
            ReturnTransitAndCommit=None,
            CarrierCodes=None,
            VariableOptions=None,
            ConsolidationKey=None,
            RequestedShipment=RequestedShipment(
                ShipTimestamp=datetime.now(),
                DropoffType=payload.shipment.extra.get("DropoffType"),
                ServiceType=ServiceType[requested_services[0]].value
                if len(requested_services) > 0
                else None,
                PackagingType=PackagingType[
                    payload.shipment.packaging_type or "YOUR_PACKAGING"
                ].value,
                VariationOptions=None,
                TotalWeight=Weight(
                    Units=payload.shipment.weight_unit,
                    Value=payload.shipment.total_weight
                    or reduce(lambda r, p: r + p.weight, payload.shipment.items, 0.0),
                ),
                TotalInsuredValue=Money(
                    Currency=payload.shipment.currency,
                    Amount=payload.shipment.insured_amount,
                )
                if payload.shipment.insured_amount != None
                else None,
                PreferredCurrency=payload.shipment.currency,
                ShipmentAuthorizationDetail=None,
                Shipper=Party(
                    AccountNumber=payload.shipper.account_number,
                    Tins=[
                        TaxpayerIdentification(
                            TinType=payload.shipper.extra.get("TinType"),
                            Usage=payload.shipper.extra.get("Usage"),
                            Number=payload.shipper.tax_id,
                            EffectiveDate=payload.shipper.extra.get("EffectiveDate"),
                            ExpirationDate=payload.shipper.extra.get("ExpirationDate"),
                        )
                    ]
                    if payload.shipper.tax_id != None
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
                        CountryName=payload.shipper.country_name,
                        Residential=None,
                        GeographicCoordinates=None,
                    ),
                ),
                Recipient=Party(
                    AccountNumber=payload.recipient.account_number,
                    Tins=[
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
                    if payload.recipient.tax_id != None
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
                        CountryName=payload.recipient.country_name,
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
                        SpecialServiceType[option.code].value for option in options
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
                SmartPostDetail=(
                    lambda smartpost: SmartPostShipmentDetail(
                        ProcessingOptionsRequested=SmartPostShipmentProcessingOptionsRequested(
                            Options=smartpost.get("ProcessingOptionsRequested").get(
                                "Options"
                            )
                        )
                        if "ProcessingOptionsRequested" in smartpost
                        else None,
                        Indicia=smartpost.get("Indicia"),
                        AncillaryEndorsement=smartpost.get("AncillaryEndorsement"),
                        HubId=smartpost.get("HubId"),
                        CustomerManifestId=smartpost.get("CustomerManifestId"),
                    )
                )(payload.shipment.extra.get("SmartPostDetail"))
                if "SmartPostDetail" in payload.shipment.extra
                else None,
                BlockInsightVisibility=None,
                LabelSpecification=LabelSpecification(
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
