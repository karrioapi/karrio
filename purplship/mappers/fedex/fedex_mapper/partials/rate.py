from pyfedex.rate_v22 import *
from datetime import datetime
from .interface import reduce, Tuple, List, E, FedexMapperBase


class FedexMapperPartial(FedexMapperBase):
    
    def parse_rate_reply(self, response: 'XMLElement') -> Tuple[List[E.QuoteDetails], List[E.Error]]:
        rate_replys = response.xpath('.//*[local-name() = $name]', name="RateReplyDetails")
        quotes = reduce(self._extract_quote, rate_replys, [])
        return (quotes, self.parse_error_response(response))

    def _extract_quote(self, quotes: List[E.QuoteDetails], detailNode: 'XMLElement') -> List[E.QuoteDetails]: 
        detail = RateReplyDetail()
        detail.build(detailNode)
        if not detail.RatedShipmentDetails:
            return quotes
        shipmentDetail = detail.RatedShipmentDetails[0].ShipmentRateDetail
        Discounts_ = map(lambda d: E.ChargeDetails(name=d.RateDiscountType, amount=float(d.Amount.Amount)), shipmentDetail.FreightDiscounts)
        Surcharges_ = map(lambda s: E.ChargeDetails(name=s.SurchargeType, amount=float(s.Amount.Amount)), shipmentDetail.Surcharges)
        Taxes_ = map(lambda t: E.ChargeDetails(name=t.TaxType, amount=float(t.Amount.Amount)), shipmentDetail.Taxes)
        return quotes + [
            E.QuoteDetails(
                carrier=self.client.carrier_name,
                service_name=detail.ServiceType,
                service_type=detail.ActualRateType,
                currency=shipmentDetail.CurrencyExchangeRate.IntoCurrency if shipmentDetail.CurrencyExchangeRate else None,
                base_charge=float(shipmentDetail.TotalBaseCharge.Amount),
                total_charge=float(shipmentDetail.TotalNetChargeWithDutiesAndTaxes.Amount),
                duties_and_taxes=float(shipmentDetail.TotalTaxes.Amount),
                discount=float(shipmentDetail.TotalFreightDiscounts.Amount),
                extra_charges=list(Discounts_) + list(Surcharges_) + list(Taxes_)
            )
        ]


    def create_rate_request(self, payload: E.shipment_request) -> RateRequest:
        return RateRequest(
            WebAuthenticationDetail=self.webAuthenticationDetail,
            ClientDetail=self.clientDetail,
            TransactionDetail=TransactionDetail(CustomerTransactionId="FTC"),
            Version=VersionId(ServiceId="crs", Major=22, Intermediate=0, Minor=0),
            ReturnTransitAndCommit=None,
            CarrierCodes=None,
            VariableOptions=None,
            ConsolidationKey=None,
            RequestedShipment=RequestedShipment(
                ShipTimestamp=datetime.now(),
                DropoffType=payload.shipment.extra.get('DropoffType'),
                ServiceType=payload.shipment.extra.get('ServiceType'),
                PackagingType=payload.shipment.packaging_type or "YOUR_PACKAGING",
                VariationOptions=None,
                TotalWeight=Weight(
                    Units=payload.shipment.weight_unit,
                    Value=payload.shipment.total_weight or reduce(lambda r, p: r + p.weight, payload.shipment.packages, 0)
                ),
                TotalInsuredValue=payload.shipment.insured_amount,
                PreferredCurrency=payload.shipment.currency,
                ShipmentAuthorizationDetail=None,
                Shipper=Party(
                    AccountNumber=payload.shipper.account_number,
                    Tins=None,
                    Contact=Contact(
                        ContactId=None,
                        PersonName=None,
                        Title=None,
                        CompanyName=payload.shipper.company_name, 
                        PhoneNumber=payload.shipper.phone_number,
                        PhoneExtension=None,
                        TollFreePhoneNumber=None,
                        PagerNumber=None,
                        FaxNumber=None,
                        EMailAddress=None
                    ) if any((payload.shipper.company_name, payload.shipper.phone_number)) else None,
                    Address=Address(
                        StreetLines=payload.shipper.address_lines,
                        City=payload.shipper.city,
                        StateOrProvinceCode=payload.shipper.state_code,
                        PostalCode=payload.shipper.postal_code,
                        UrbanizationCode=None,
                        CountryCode=payload.shipper.country_code,
                        CountryName=payload.shipper.country_name,
                        Residential=None,
                        GeographicCoordinates=None
                    )
                ),
                Recipient=Party(
                    AccountNumber=payload.recipient.extra.get('AccountNumber'),
                    Tins=None,
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
                        EMailAddress=payload.recipient.email_address
                    ) if any((payload.recipient.company_name, payload.recipient.phone_number)) else None,
                    Address=Address(
                        StreetLines=payload.recipient.address_lines,
                        City=payload.recipient.city,
                        StateOrProvinceCode=payload.recipient.state_code,
                        PostalCode=payload.recipient.postal_code,
                        UrbanizationCode=None,
                        CountryCode=payload.recipient.country_code,
                        CountryName=payload.recipient.country_name,
                        Residential=None,
                        GeographicCoordinates=None
                    )
                ),
                RecipientLocationNumber=None,
                Origin=None,
                SoldTo=None,
                ShippingChargesPayment=Payment(
                    PaymentType=payload.shipment.paid_by or "SENDER",
                    Payor=(
                        Payor(ResponsibleParty=Party(
                            AccountNumber=payload.shipment.payment_account_number,
                            Tins=None,
                            Contact=None,
                            Address=None
                        )) if payload.shipment.payment_account_number is not None else None
                    )
                ) if any((payload.shipment.paid_by, payload.shipment.payment_account_number)) else None,
                SpecialServicesRequested=ShipmentSpecialServicesRequested(
                    SpecialServiceTypes=payload.shipment.services,
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
                    CustomDeliveryWindowDetail=None
                ) if len(payload.shipment.services) > 0 else None,
                ExpressFreightDetail=None,
                FreightShipmentDetail=None,
                DeliveryInstructions=None,
                VariableHandlingChargeDetail=None,
                CustomsClearanceDetail=None,
                PickupDetail=None,
                SmartPostDetail=(lambda smartpost: SmartPostShipmentDetail(
                    ProcessingOptionsRequested=SmartPostShipmentProcessingOptionsRequested(
                        Options=smartpost.get('ProcessingOptionsRequested').get('Options')
                    ) if 'ProcessingOptionsRequested' in smartpost else None,
                    Indicia=smartpost.get('Indicia'),
                    AncillaryEndorsement=smartpost.get('AncillaryEndorsement'),
                    HubId=smartpost.get('HubId'),
                    CustomerManifestId=smartpost.get('CustomerManifestId')
                ))(payload.shipment.extra.get('SmartPostDetail')) if 'SmartPostDetail' in payload.shipment.extra else None,
                BlockInsightVisibility=None,
                LabelSpecification=None,
                ShippingDocumentSpecification=None,
                RateRequestTypes=(
                    ["LIST"] + 
                    ([] if not payload.shipment.currency else ["PREFERRED"])
                ),
                EdtRequestType=payload.shipment.extra.get('EdtRequestType'),
                PackageCount=len(payload.shipment.packages),
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
                            Units=payload.shipment.weight_unit,
                            Value=pkg.weight
                        ),
                        Dimensions=Dimensions(
                            Length=pkg.length,
                            Width=pkg.width,
                            Height=pkg.height,
                            Units=payload.shipment.dimension_unit
                        ),
                        PhysicalPackaging=None,
                        ItemDescription=pkg.description,
                        ItemDescriptionForClearance=None,
                        CustomerReferences=None,
                        SpecialServicesRequested=None,
                        ContentRecords=None
                    ) for index, pkg in enumerate(payload.shipment.packages)
                ],
            )
        )
