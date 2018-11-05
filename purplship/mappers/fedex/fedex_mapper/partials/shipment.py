from pyfedex.ship_service_v21 import *
from base64 import b64encode
from datetime import datetime
from .interface import reduce, Tuple, List, E, FedexMapperBase


class FedexMapperPartial(FedexMapperBase):

    def parse_process_shipment_reply(self, response: 'XMLElement') -> Tuple[E.ShipmentDetails, List[E.Error]]:
        details = response.xpath('.//*[local-name() = $name]', name="CompletedShipmentDetail")
        shipment = self._extract_shipment(details[0]) if len(details) > 0 else None
        return (shipment, self.parse_error_response(response))

    def _extract_shipment(self, shipmentDetailNode: 'XMLElement') -> E.ShipmentDetails:
        detail = CompletedShipmentDetail()
        detail.build(shipmentDetailNode)

        def get_rateDetail() -> ShipmentRateDetail:
            return detail.ShipmentRating.ShipmentRateDetails[0]

        def get_items() -> List[CompletedPackageDetail]:
            return detail.CompletedPackageDetails

        shipment = get_rateDetail()
        items = get_items()

        return E.ShipmentDetails(
            carrier=self.client.carrier_name,
            tracking_numbers=reduce(
                lambda ids, pkg: ids + [id.TrackingNumber for id in pkg.TrackingIds], items, []
            ),
            total_charge=E.ChargeDetails(
                name="Shipment charge",
                amount=shipment.TotalNetChargeWithDutiesAndTaxes.Amount,
                currency=shipment.TotalNetChargeWithDutiesAndTaxes.Currency
            ),
            charges=[E.ChargeDetails(
                    name="base_charge",
                    amount=shipment.TotalBaseCharge.Amount,
                    currency=shipment.TotalBaseCharge.Currency
            ), E.ChargeDetails(
                    name="discount",
                    amount=detail.ShipmentRating.EffectiveNetDiscount.Amount,
                    currency=detail.ShipmentRating.EffectiveNetDiscount.Currency
            )] + 
            [E.ChargeDetails(
                    name=surcharge.SurchargeType,
                    amount=surcharge.Amount.Amount,
                    currency=surcharge.Amount.Currency
            ) for surcharge in shipment.Surcharges] + 
            [E.ChargeDetails(
                    name=fee.Type,
                    amount=fee.Amount.Amount,
                    currency=fee.Amount.Currency
            ) for fee in shipment.AncillaryFeesAndTaxes],
            services=[
                detail.ServiceTypeDescription
            ],
            documents=reduce(
               lambda labels, pkg: labels + [str(b64encode(part.Image), 'utf-8') for part in pkg.Label.Parts], items, []
            )
        )

    def create_process_shipment_request(self, payload: E.shipment_request) -> ProcessShipmentRequest:
        return ProcessShipmentRequest(
            WebAuthenticationDetail=self.webAuthenticationDetail,
            ClientDetail=self.clientDetail,
            TransactionDetail=TransactionDetail(CustomerTransactionId="IE_v18_Ship"),
            Version=VersionId(ServiceId="ship", Major=21, Intermediate=0, Minor=0),
            RequestedShipment=RequestedShipment(
                ShipTimestamp=datetime.now(),
                DropoffType=payload.shipment.extra.get('DropoffType'),
                ServiceType=payload.shipment.extra.get('ServiceType'),
                PackagingType=payload.shipment.packaging_type or "YOUR_PACKAGING",
                ManifestDetail=None,
                TotalWeight=Weight(
                    Units=payload.shipment.weight_unit,
                    Value=payload.shipment.total_weight or reduce(lambda r, p: r + p.weight, payload.shipment.items, 0)
                ),
                TotalInsuredValue=payload.shipment.insured_amount,
                PreferredCurrency=payload.shipment.currency,
                ShipmentAuthorizationDetail=None,
                Shipper=Party(
                    AccountNumber=payload.shipper.account_number,
                    Tins=None,
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
                        EMailAddress=payload.shipper.email_address
                    ) if any((payload.shipper.company_name, payload.shipper.phone_number, payload.shipper.person_name, payload.shipper.email_address)) else None,
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
                    ) if any((payload.recipient.company_name, payload.recipient.phone_number, payload.recipient.person_name, payload.recipient.email_address)) else None,
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
                    Payor=(lambda payor:
                        Payor(ResponsibleParty=Party(
                            AccountNumber=payload.shipment.payment_account_number,
                            Tins=[
                                TaxpayerIdentification(
                                    TinType=tin.get('TinType'),
                                    Number=tin.get('Number'),
                                    Usage=tin.get('Usage'),
                                    EffectiveDate=tin.get('EffectiveDate'),
                                    ExpirationDate=tin.get('ExpirationDate'),
                                ) for tin in payor.extra.get('Tins')
                            ] if 'Tins' in payor.extra else None,
                            Contact=Contact(
                                ContactId=payor.extra.get('ContactId'),
                                PersonName=payor.person_name,
                                Title=None,
                                CompanyName=payor.company_name, 
                                PhoneNumber=payor.phone_number,
                                PhoneExtension=None,
                                TollFreePhoneNumber=None,
                                PagerNumber=None,
                                FaxNumber=None,
                                EMailAddress=payor.email_address
                            ) if any((payor.company_name, payor.phone_number, payor.person_name, payor.email_address)) else None,
                            Address=Address(
                                StreetLines=payor.address_lines,
                                City=payor.city,
                                StateOrProvinceCode=payor.state_code,
                                PostalCode=payor.postal_code,
                                UrbanizationCode=None,
                                CountryCode=payor.country_code,
                                CountryName=payor.country_name,
                                Residential=None,
                                GeographicCoordinates=None
                            ) if any((payor.country_code, payor.country_name, payor.address_lines, payor.city, payor.state_code, payor.postal_code)) else None
                        )) if payload.shipment.payment_account_number is not None else None
                    )(E.party(
                        **payload.shipment.extra.get('Payor').get('ResponsibleParty')
                    )) if 'Payor' in payload.shipment.extra else None
                ) if any((payload.shipment.paid_by, payload.shipment.payment_account_number)) else None,
                SpecialServicesRequested=ShipmentSpecialServicesRequested(
                    SpecialServiceTypes=payload.shipment.extra_services,
                    CodDetail=None,
                    DeliveryOnInvoiceAcceptanceDetail=None,
                    HoldAtLocationDetail=None,
                    EventNotificationDetail=None,
                    ReturnShipmentDetail=None,
                    PendingShipmentDetail=None,
                    InternationalControlledExportDetail=None,
                    InternationalTrafficInArmsRegulationsDetail=(
                        InternationalTrafficInArmsRegulationsDetail(
                            LicenseOrExemptionNumber=payload.shipment.extra.get('SpecialServicesRequested').get('InternationalTrafficInArmsRegulationsDetail').get('LicenseOrExemptionNumber')
                        )
                    ) if 'SpecialServicesRequested' in payload.shipment.extra and 'InternationalTrafficInArmsRegulationsDetail' in payload.shipment.extra.get('SpecialServicesRequested') else None ,
                    ShipmentDryIceDetail=None,
                    HomeDeliveryPremiumDetail=None,
                    FreightGuaranteeDetail=None,
                    EtdDetail=None,
                    CustomDeliveryWindowDetail=None
                ) if len(payload.shipment.extra_services) > 0 else None,
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
                LabelSpecification=LabelSpecification(
                    Dispositions=payload.shipment.label.extra.get('Dispositions'),
                    LabelFormatType=payload.shipment.label.format,
                    ImageType=payload.shipment.label.type,
                    LabelStockType=payload.shipment.label.extra.get('LabelStockType'),
                    LabelPrintingOrientation=payload.shipment.label.extra.get('LabelPrintingOrientation'),
                    LabelOrder=payload.shipment.label.extra.get('LabelOrder'),
                    PrintedLabelOrigin=payload.shipment.label.extra.get('PrintedLabelOrigin'),
                    CustomerSpecifiedDetail=None
                ) if payload.shipment.label is not None else None,
                ShippingDocumentSpecification=None,
                RateRequestTypes=(
                    ["LIST"] + 
                    ([] if not payload.shipment.currency else ["PREFERRED"])
                ),
                EdtRequestType=payload.shipment.extra.get('EdtRequestType'),
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
                        ItemDescription=pkg.content,
                        ItemDescriptionForClearance=None,
                        CustomerReferences=[
                            CustomerReference(
                                CustomerReferenceType=ref.get('CustomerReferenceType'),
                                Value=ref.get('Value')
                            ) for ref in pkg.extra.get('CustomerReferences')
                        ] if 'CustomerReferences' in pkg.extra else None,
                        SpecialServicesRequested=None,
                        ContentRecords=None
                    ) for index, pkg in enumerate(payload.shipment.items)
                ]
            ),
        )
