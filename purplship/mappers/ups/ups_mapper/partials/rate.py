import time
from pyups import (
    freight_rate as Rate,
    package_rate as PRate,
    common as Common
)
from .interface import reduce, Tuple, List, T, UPSMapperBase
from purplship.domain.Types.units import DimensionUnit
from purplship.mappers.ups.ups_units import (
    RatingServiceCode,
    RatingPackagingType,
    WeightUnit,
    PackagingType
)


class UPSMapperPartial(UPSMapperBase):
    
    def parse_freight_rate_response(self, response: 'XMLElement') -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        rate_replys = response.xpath('.//*[local-name() = $name]', name="FreightRateResponse")
        rates = reduce(self._extract_freight_rate, rate_replys, [])
        return (rates, self.parse_error_response(response))

    def _extract_freight_rate(self, rates: List[T.QuoteDetails], detailNode: 'XMLElement') -> List[T.QuoteDetails]: 
        detail = Rate.FreightRateResponse()
        detail.build(detailNode)

        total_charge = [r for r in detail.Rate if r.Type.Code == 'AFTR_DSCNT'][0]
        Discounts_ = [T.ChargeDetails(name=r.Type.Code, currency=r.Factor.UnitOfMeasurement.Code, amount=float(r.Factor.Value)) for r in detail.Rate if r.Type.Code == 'DSCNT']
        Surcharges_ = [T.ChargeDetails(name=r.Type.Code, currency=r.Factor.UnitOfMeasurement.Code, amount=float(r.Factor.Value)) for r in detail.Rate if r.Type.Code not in ['DSCNT', 'AFTR_DSCNT', 'DSCNT_RATE', 'LND_GROSS']]
        extra_charges = Discounts_ + Surcharges_
        return rates + [
            T.QuoteDetails(
                carrier=self.client.carrier_name, 
                currency=detail.TotalShipmentCharge.CurrencyCode,
                service_name=detail.Service.Description,
                service_type=detail.Service.Code,
                base_charge=float(detail.TotalShipmentCharge.MonetaryValue),
                total_charge=float(total_charge.Factor.Value or 0),
                duties_and_taxes=reduce(lambda r, c: r + c.amount, Surcharges_, 0),
                discount=reduce(lambda r, c: r + c.amount, Discounts_, 0),
                extra_charges=extra_charges
            )
        ]
    
    def parse_package_rate_response(self, response: 'XMLElement') -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        rate_replys = response.xpath('.//*[local-name() = $name]', name="RatedShipment")
        rates = reduce(self._extract_package_rate, rate_replys, [])
        return (rates, self.parse_error_response(response))

    def _extract_package_rate(self, rates: List[T.QuoteDetails], detailNode: 'XMLElement') -> List[T.QuoteDetails]: 
        rate = PRate.RatedShipmentType()
        rate.build(detailNode)

        if rate.NegotiatedRateCharges != None:
            total_charges = rate.NegotiatedRateCharges.TotalChargesWithTaxes or rate.NegotiatedRateCharges.TotalCharge
            taxes = rate.NegotiatedRateCharges.TaxCharges
            itemized_charges = rate.NegotiatedRateCharges.ItemizedCharges + taxes
        else:
            total_charges = rate.TotalChargesWithTaxes or rate.TotalCharges
            taxes = rate.TaxCharges
            itemized_charges = rate.ItemizedCharges + taxes

        extra_charges = itemized_charges + [ rate.ServiceOptionsCharges ] 
        
        return rates + [
            T.QuoteDetails(
                carrier=self.client.carrier_name, 
                currency=rate.TransportationCharges.CurrencyCode,
                service_name=rate.Service.Description,
                service_type=rate.Service.Code,
                base_charge=float(rate.TransportationCharges.MonetaryValue),
                total_charge=float(total_charges.MonetaryValue),
                duties_and_taxes=reduce(
                    lambda total, charge: total + float(charge.MonetaryValue),
                    taxes or [], 
                    0
                ),
                discount=None,
                extra_charges=reduce(
                    lambda total, charge: total + [T.ChargeDetails(
                        name=charge.Code,
                        amount=float(charge.MonetaryValue),
                        currency=charge.CurrencyCode
                    )],
                    [charge for charge in extra_charges if charge != None],
                    []
                )
            )
        ]


    def create_freight_rate_request(self, payload: T.shipment_request) -> Rate.FreightRateRequest:
        service = (
            [RatingServiceCode[svc] for svc in payload.shipment.services if svc in RatingServiceCode.__members__] + 
            [RatingServiceCode.UPS_Freight_LTL_Guaranteed]
        )[0]
        return Rate.FreightRateRequest(
            Request=Common.RequestType(
                TransactionReference=Common.TransactionReferenceType(
                    TransactionIdentifier="TransactionIdentifier"
                ),
                RequestOption=[1]
            ),
            ShipFrom=Rate.ShipFromType(
                Name=payload.shipper.company_name,
                Address=Rate.AddressType(
                    City=payload.shipper.city,
                    PostalCode=payload.shipper.postal_code,
                    CountryCode=payload.shipper.country_code,
                    AddressLine=payload.shipper.address_lines
                ),
                AttentionName=payload.shipper.person_name,
            ),
            ShipTo=Rate.ShipToType(
                Name=payload.recipient.company_name,
                Address=Rate.AddressType(
                    City=payload.recipient.city,
                    PostalCode=payload.recipient.postal_code,
                    CountryCode=payload.recipient.country_code,
                    AddressLine=payload.recipient.address_lines
                ),
                AttentionName=payload.recipient.person_name,
            ),
            PaymentInformation=Rate.PaymentInformationType(
                Payer=Rate.PayerType(
                    Name=payload.shipment.payment_country_code or payload.shipper.country_code,
                    Address=Rate.AddressType(
                        City=payload.shipper.city,
                        PostalCode=payload.shipper.postal_code,
                        CountryCode=payload.shipper.country_code,
                        AddressLine=payload.shipper.address_lines
                    ),
                    ShipperNumber=payload.shipper.account_number or payload.shipment.payment_account_number or self.client.account_number
                ),
                ShipmentBillingOption=Rate.RateCodeDescriptionType(Code=10)
            ),
            Service=Rate.RateCodeDescriptionType(Code=service.value, Description=None),
            HandlingUnitOne=Rate.HandlingUnitType(
                Quantity=1, 
                Type=Rate.RateCodeDescriptionType(Code="SKD")
            ),
            ShipmentServiceOptions=Rate.ShipmentServiceOptionsType(
                PickupOptions=Rate.PickupOptionsType(WeekendPickupIndicator="")
            ),
            DensityEligibleIndicator="",
            AdjustedWeightIndicator="",
            HandlingUnitWeight=Rate.HandlingUnitWeightType(
                Value=1,
                UnitOfMeasurement=Rate.UnitOfMeasurementType(
                    Code=WeightUnit[payload.shipment.weight_unit].value
                )
            ),
            PickupRequest=None,
            GFPOptions=Rate.OnCallInformationType(),
            TimeInTransitIndicator="",
            Commodity=[
                Rate.CommodityType(
                    Description=c.description or "...",
                    Weight=Rate.WeightType(
                        UnitOfMeasurement=Rate.UnitOfMeasurementType(
                            Code=WeightUnit[payload.shipment.weight_unit].value
                        ),
                        Value=c.weight
                    ),
                    Dimensions=Rate.DimensionsType(
                        UnitOfMeasurement=Rate.UnitOfMeasurementType(
                            Code=DimensionUnit[payload.shipment.dimension_unit].value
                        ),
                        Width=c.width,
                        Height=c.height,
                        Length=c.length
                    ),
                    NumberOfPieces=len(payload.shipment.items),
                    PackagingType=Rate.RateCodeDescriptionType(
                        Code=PackagingType[c.packaging_type or "BOX"].value, 
                        Description=None
                    ),
                    FreightClass=50
                ) for c in payload.shipment.items
            ]
        )

    def create_package_rate_request(self, payload: T.shipment_request) -> PRate.RateRequest:
        service = (
            [RatingServiceCode[svc] for svc in payload.shipment.services if svc in RatingServiceCode.__members__] + 
            [RatingServiceCode.UPS_Worldwide_Express]
        )[0]
        payment_details_provided = (
            all((payload.shipment.paid_by, payload.shipment.payment_account_number)) or
            (payload.shipment.paid_by == 'SENDER' and payload.shipper.account_number != None) or 
            (payload.shipment.paid_by == 'RECIPIENT' and payload.recipient.account_number != None)
        )
        return PRate.RateRequest(
            Request=Common.RequestType(
                RequestOption=payload.shipment.extra.get('RequestOption') or ["Rate"],
                SubVersion=None,
                TransactionReference=Common.TransactionReferenceType(
                    CustomerContext=', '.join(payload.shipment.references),
                    TransactionIdentifier=payload.shipment.extra.get('TransactionIdentifier')
                )
            ),
            PickupType=None,
            CustomerClassification=None,
            Shipment=PRate.ShipmentType(
                OriginRecordTransactionTimestamp=None,
                Shipper=PRate.ShipperType(
                    Name=payload.shipper.company_name,
                    ShipperNumber=payload.shipper.account_number,
                    Address=PRate.ShipAddressType(
                        AddressLine=payload.shipper.address_lines,
                        City=payload.shipper.city,
                        StateProvinceCode=payload.shipper.state_code,
                        PostalCode=payload.shipper.postal_code,
                        CountryCode=payload.shipper.country_code
                    )
                ),
                ShipTo=PRate.ShipToType(
                    Name=payload.recipient.company_name,
                    Address=PRate.ShipToAddressType(
                        AddressLine=payload.recipient.address_lines,
                        City=payload.recipient.city,
                        StateProvinceCode=payload.recipient.state_code,
                        PostalCode=payload.recipient.postal_code,
                        CountryCode=payload.recipient.country_code,
                        ResidentialAddressIndicator=None
                    )
                ),
                ShipFrom=(lambda shipFrom:
                    PRate.ShipFromType(
                        Name=shipFrom.company_name,
                        Address=PRate.ShipAddressType(
                            AddressLine=shipFrom.address_lines,
                            City=shipFrom.city,
                            StateProvinceCode=shipFrom.state_code,
                            PostalCode=shipFrom.postal_code,
                            CountryCode=shipFrom.country_code
                        )
                    )
                )(T.party(**payload.shipment.extra.get('ShipFrom'))) if 'ShipFrom' in payload.shipment.extra else None,
                AlternateDeliveryAddress=(lambda alternate:
                    PRate.AlternateDeliveryAddressType(
                        Name=alternate.companyName,
                        Address=PRate.ShipAddressType(
                            AddressLine=alternate.address_lines,
                            City=alternate.city,
                            StateProvinceCode=alternate.state_code,
                            PostalCode=alternate.postal_code,
                            CountryCode=alternate.country_code
                        )
                    )
                )(T.party(**payload.shipment.extra.get('AlternateDeliveryAddress'))) if 'AlternateDeliveryAddress' in payload.shipment.extra else None,
                ShipmentIndicationType=None,
                PaymentDetails=PRate.PaymentDetailsType(
                    ShipmentCharge=[
                        PRate.ShipmentChargeType(
                            Type=None,
                            BillShipper=PRate.BillShipperChargeType(
                                AccountNumber=payload.shipment.payment_account_number or payload.shipper.account_number
                            ) if payload.shipment.paid_by == 'SENDER' else None,
                            BillReceiver=PRate.BillReceiverChargeType(
                                AccountNumber=payload.shipment.payment_account_number or payload.recipient.account_number,
                                Address=PRate.BillReceiverAddressType(
                                    PostalCode=payload.recipient.postal_code
                                )
                            ) if payload.shipment.paid_by == 'RECIPIENT' else None,
                            BillThirdParty=PRate.BillThirdPartyChargeType(
                                AccountNumber=payload.shipment.payment_account_number,
                                Address=PRate.BillReceiverAddressType(
                                    PostalCode=payload.shipment.extra.get('payor_postal_code')
                                )
                            ) if payload.shipment.paid_by == 'THIRD_PARTY' else None,
                            ConsigneeBilledIndicator=None
                        )
                    ],
                    SplitDutyVATIndicator=None
                ) if payment_details_provided else None,
                FRSPaymentInformation=None,
                FreightShipmentInformation=None,
                GoodsNotInFreeCirculationIndicator=None,
                Service=PRate.UOMCodeDescriptionType(Code=service.value, Description=None),
                NumOfPieces=payload.shipment.total_items,
                ShipmentTotalWeight=payload.shipment.total_weight,
                DocumentsOnlyIndicator="" if payload.shipment.is_document else None,
                Package=[
                    PRate.PackageType(
                        PackagingType=PRate.UOMCodeDescriptionType(
                            Code=RatingPackagingType[pkg.packaging_type or "BOX"].value,
                            Description=None
                        ),
                        Dimensions=PRate.DimensionsType(
                            UnitOfMeasurement=PRate.UOMCodeDescriptionType(
                                Code=DimensionUnit[payload.shipment.dimension_unit].value,
                                Description=None
                            ),
                            Length=pkg.length,
                            Width=pkg.width,
                            Height=pkg.height
                        ),
                        DimWeight=pkg.extra.get('DimWeight'),
                        PackageWeight=PRate.PackageWeightType(
                            UnitOfMeasurement=PRate.UOMCodeDescriptionType(
                                Code=WeightUnit[payload.shipment.weight_unit].value,
                                Description=None
                            ),
                            Weight=pkg.weight
                        ),
                        Commodity=None,
                        PackageServiceOptions=None,
                        AdditionalHandlingIndicator=None
                    ) for pkg in payload.shipment.items
                ],
                ShipmentServiceOptions=None,
                ShipmentRatingOptions=(lambda rating:
                    PRate.ShipmentRatingOptionsType(
                        NegotiatedRatesIndicator="" if 'NegotiatedRatesIndicator' in rating else None,
                        FRSShipmentIndicator="" if 'FRSShipmentIndicator' in rating else None,
                        RateChartIndicator="" if 'RateChartIndicator' in rating else None,
                        UserLevelDiscountIndicator="" if 'UserLevelDiscountIndicator' in rating else None
                    )
                )(payload.shipment.extra.get('ShipmentRatingOptions')) if 'ShipmentRatingOptions' in payload.shipment.extra else None,
                InvoiceLineTotal=None,
                RatingMethodRequestedIndicator=None,
                TaxInformationIndicator=None,
                PromotionalDiscountInformation=None,
                DeliveryTimeInformation=None
            )
        )

