from lxml import etree
from pyups import package_rate as PRate, common as Common
from .interface import reduce, Tuple, List, T, UPSMapperBase
from purplship.domain.Types.units import DimensionUnit
from purplship.mappers.ups.ups_units import (
    RatingServiceCode,
    RatingPackagingType,
    WeightUnit,
    ServiceOption,
    RatingOption,
    ShippingServiceCode
)


class UPSMapperPartial(UPSMapperBase):

    def parse_package_rate_response(
        self, response: etree.ElementBase
    ) -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        rate_replys = response.xpath(".//*[local-name() = $name]", name="RatedShipment")
        rates: List[T.QuoteDetails] = reduce(
            self._extract_package_rate, rate_replys, []
        )
        return (rates, self.parse_error_response(response))

    def _extract_package_rate(
        self, rates: List[T.QuoteDetails], detailNode: etree.ElementBase
    ) -> List[T.QuoteDetails]:
        rate = PRate.RatedShipmentType()
        rate.build(detailNode)

        if rate.NegotiatedRateCharges != None:
            total_charges = (
                rate.NegotiatedRateCharges.TotalChargesWithTaxes
                or rate.NegotiatedRateCharges.TotalCharge
            )
            taxes = rate.NegotiatedRateCharges.TaxCharges
            itemized_charges = rate.NegotiatedRateCharges.ItemizedCharges + taxes
        else:
            total_charges = rate.TotalChargesWithTaxes or rate.TotalCharges
            taxes = rate.TaxCharges
            itemized_charges = rate.ItemizedCharges + taxes

        extra_charges = itemized_charges + [rate.ServiceOptionsCharges]

        arrival = PRate.PickupType()
        [
            arrival.build(arrival) for arrival in
            detailNode.xpath(".//*[local-name() = $name]", name="Arrival")
        ]
        currency_ = next(c.text for c in detailNode.xpath(
            ".//*[local-name() = $name]", name="CurrencyCode"
        ))

        return rates + [
            T.QuoteDetails(
                carrier=self.client.carrier_name,
                currency=currency_,
                service_name=str(ShippingServiceCode(rate.Service.Code).name),
                service_type=rate.Service.Code,
                base_charge=float(rate.TransportationCharges.MonetaryValue),
                total_charge=float(total_charges.MonetaryValue),
                duties_and_taxes=reduce(
                    lambda total, charge: total + float(charge.MonetaryValue),
                    taxes or [],
                    0.0,
                ),
                discount=None,
                extra_charges=reduce(
                    lambda total, charge: total
                    + [
                        T.ChargeDetails(
                            name=charge.Code,
                            amount=float(charge.MonetaryValue),
                            currency=charge.CurrencyCode,
                        )
                    ],
                    [charge for charge in extra_charges if charge != None],
                    [],
                ),
                delivery_date=str(arrival.Date)
            )
        ]

    def create_package_rate_request(
        self, payload: T.ShipmentRequest
    ) -> PRate.RateRequest:
        service = (
            [
                RatingServiceCode[svc]
                for svc in payload.shipment.services
                if svc in RatingServiceCode.__members__
            ]
            + [RatingServiceCode.UPS_Worldwide_Express]
        )[0]
        payment_details_provided = (
            all((payload.shipment.paid_by, payload.shipment.payment_account_number))
            or (
                payload.shipment.paid_by == "SENDER"
                and payload.shipper.account_number != None
            )
            or (
                payload.shipment.paid_by == "RECIPIENT"
                and payload.recipient.account_number != None
            )
        )
        is_negotiated_rate = any(
            (payload.shipment.payment_account_number, payload.shipper.account_number)
        )
        service_options = [
            opt
            for opt in payload.shipment.options
            if opt.code in ServiceOption.__members__
        ]
        rating_options = [
            opt
            for opt in payload.shipment.options
            if opt.code in RatingOption.__members__
        ]
        return PRate.RateRequest(
            Request=Common.RequestType(
                RequestOption=payload.shipment.extra.get("RequestOption") or ["Rate"],
                SubVersion=None,
                TransactionReference=Common.TransactionReferenceType(
                    CustomerContext=", ".join(payload.shipment.references),
                    TransactionIdentifier=payload.shipment.extra.get(
                        "TransactionIdentifier"
                    ),
                ),
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
                        CountryCode=payload.shipper.country_code,
                    ),
                ),
                ShipTo=PRate.ShipToType(
                    Name=payload.recipient.company_name,
                    Address=PRate.ShipToAddressType(
                        AddressLine=payload.recipient.address_lines,
                        City=payload.recipient.city,
                        StateProvinceCode=payload.recipient.state_code,
                        PostalCode=payload.recipient.postal_code,
                        CountryCode=payload.recipient.country_code,
                        ResidentialAddressIndicator=None,
                    ),
                ),
                ShipFrom=(
                    lambda shipFrom: PRate.ShipFromType(
                        Name=shipFrom.company_name,
                        Address=PRate.ShipAddressType(
                            AddressLine=shipFrom.address_lines,
                            City=shipFrom.city,
                            StateProvinceCode=shipFrom.state_code,
                            PostalCode=shipFrom.postal_code,
                            CountryCode=shipFrom.country_code,
                        ),
                    )
                )(T.Party(**payload.shipment.extra.get("ShipFrom")))
                if "ShipFrom" in payload.shipment.extra
                else None,
                AlternateDeliveryAddress=(
                    lambda alternate: PRate.AlternateDeliveryAddressType(
                        Name=alternate.company_name,
                        Address=PRate.ShipAddressType(
                            AddressLine=alternate.address_lines,
                            City=alternate.city,
                            StateProvinceCode=alternate.state_code,
                            PostalCode=alternate.postal_code,
                            CountryCode=alternate.country_code,
                        ),
                    )
                )(T.Party(**payload.shipment.extra.get("AlternateDeliveryAddress")))
                if "AlternateDeliveryAddress" in payload.shipment.extra
                else None,
                ShipmentIndicationType=None,
                PaymentDetails=PRate.PaymentDetailsType(
                    ShipmentCharge=[
                        PRate.ShipmentChargeType(
                            Type=None,
                            BillShipper=PRate.BillShipperChargeType(
                                AccountNumber=payload.shipment.payment_account_number
                                or payload.shipper.account_number
                            )
                            if payload.shipment.paid_by == "SENDER"
                            else None,
                            BillReceiver=PRate.BillReceiverChargeType(
                                AccountNumber=payload.shipment.payment_account_number
                                or payload.recipient.account_number,
                                Address=PRate.BillReceiverAddressType(
                                    PostalCode=payload.recipient.postal_code
                                ),
                            )
                            if payload.shipment.paid_by == "RECIPIENT"
                            else None,
                            BillThirdParty=PRate.BillThirdPartyChargeType(
                                AccountNumber=payload.shipment.payment_account_number,
                                Address=PRate.BillReceiverAddressType(
                                    PostalCode=payload.shipment.extra.get(
                                        "payor_postal_code"
                                    )
                                ),
                            )
                            if payload.shipment.paid_by == "THIRD_PARTY"
                            else None,
                            ConsigneeBilledIndicator=None,
                        )
                    ],
                    SplitDutyVATIndicator=None,
                )
                if payment_details_provided
                else None,
                FRSPaymentInformation=None,
                FreightShipmentInformation=None,
                GoodsNotInFreeCirculationIndicator=None,
                Service=PRate.UOMCodeDescriptionType(
                    Code=service.value, Description=None
                ),
                NumOfPieces=payload.shipment.total_items,
                ShipmentTotalWeight=payload.shipment.total_weight,
                DocumentsOnlyIndicator="" if payload.shipment.is_document else None,
                Package=[
                    PRate.PackageType(
                        PackagingType=PRate.UOMCodeDescriptionType(
                            Code=RatingPackagingType[pkg.packaging_type or "BOX"].value,
                            Description=None,
                        ),
                        Dimensions=PRate.DimensionsType(
                            UnitOfMeasurement=PRate.UOMCodeDescriptionType(
                                Code=DimensionUnit[
                                    payload.shipment.dimension_unit
                                ].value,
                                Description=None,
                            ),
                            Length=pkg.length,
                            Width=pkg.width,
                            Height=pkg.height,
                        ),
                        DimWeight=pkg.extra.get("DimWeight"),
                        PackageWeight=PRate.PackageWeightType(
                            UnitOfMeasurement=PRate.UOMCodeDescriptionType(
                                Code=WeightUnit[payload.shipment.weight_unit].value,
                                Description=None,
                            ),
                            Weight=pkg.weight,
                        ),
                        Commodity=None,
                        PackageServiceOptions=None,
                        AdditionalHandlingIndicator=None,
                    )
                    for pkg in payload.shipment.items
                ],
                ShipmentServiceOptions=PRate.ShipmentServiceOptionsType(
                    SaturdayDeliveryIndicator=next(
                        (
                            ""
                            for o in service_options
                            if o.code == "SaturdayDeliveryIndicator"
                        ),
                        None,
                    ),
                    AccessPointCOD=(
                        lambda option: PRate.ShipmentServiceOptionsAccessPointCODType(
                            CurrencyCode=option.value.get("CurrencyCode"),
                            MonetaryValue=option.value.get("MonetaryValue"),
                        )
                        if option != None
                        else None
                    )(
                        next(
                            (o for o in service_options if o.code == "AccessPointCOD"),
                            None,
                        )
                    ),
                    DeliverToAddresseeOnlyIndicator=next(
                        (
                            ""
                            for o in service_options
                            if o.code == "DeliverToAddresseeOnlyIndicator"
                        ),
                        None,
                    ),
                    DirectDeliveryOnlyIndicator=next(
                        (
                            ""
                            for o in service_options
                            if o.code == "DirectDeliveryOnlyIndicator"
                        ),
                        None,
                    ),
                    COD=(
                        lambda option: PRate.CODType(
                            CODFundsCode=option.value.get("CODFundsCode"),
                            CODAmount=option.value.get("CODAmount"),
                        )
                        if option != None
                        else None
                    )(next((o for o in service_options if o.code == "COD"), None)),
                    DeliveryConfirmation=(
                        lambda option: PRate.DeliveryConfirmationType(
                            DCISType=option.value.get("DCISType")
                        )
                        if option != None
                        else None
                    )(
                        next(
                            (
                                o
                                for o in service_options
                                if o.code == "DeliveryConfirmation"
                            ),
                            None,
                        )
                    ),
                    ReturnOfDocumentIndicator=next(
                        (
                            ""
                            for o in service_options
                            if o.code == "ReturnOfDocumentIndicator"
                        ),
                        None,
                    ),
                    UPScarbonneutralIndicator=next(
                        (
                            ""
                            for o in service_options
                            if o.code == "UPScarbonneutralIndicator"
                        ),
                        None,
                    ),
                    CertificateOfOriginIndicator=next(
                        (
                            ""
                            for o in service_options
                            if o.code == "CertificateOfOriginIndicator"
                        ),
                        None,
                    ),
                    PickupOptions=(
                        lambda option: PRate.PickupOptionsType(
                            LiftGateAtPickupIndicator=option.value.get(
                                "LiftGateAtPickupIndicator"
                            ),
                            HoldForPickupIndicator=option.value.get(
                                "HoldForPickupIndicator"
                            ),
                        )
                        if option != None
                        else None
                    )(
                        next(
                            (o for o in service_options if o.code == "PickupOptions"),
                            None,
                        )
                    ),
                    DeliveryOptions=(
                        lambda option: PRate.DeliveryOptionsType(
                            LiftGateAtDeliveryIndicator=option.value.get(
                                "LiftGateAtDeliveryIndicator"
                            ),
                            DropOffAtUPSFacilityIndicator=option.value.get(
                                "DropOffAtUPSFacilityIndicator"
                            ),
                        )
                        if option != None
                        else None
                    )(
                        next(
                            (o for o in service_options if o.code == "DeliveryOptions"),
                            None,
                        )
                    ),
                    RestrictedArticles=None,
                    ShipperExportDeclarationIndicator=next(
                        (
                            ""
                            for o in service_options
                            if o.code == "ShipperExportDeclarationIndicator"
                        ),
                        None,
                    ),
                    CommercialInvoiceRemovalIndicator=next(
                        (
                            ""
                            for o in service_options
                            if o.code == "CommercialInvoiceRemovalIndicator"
                        ),
                        None,
                    ),
                    ImportControl=None,
                    ReturnService=None,
                    SDLShipmentIndicator=next(
                        (
                            ""
                            for o in service_options
                            if o.code == "SDLShipmentIndicator"
                        ),
                        None,
                    ),
                    EPRAIndicator=next(
                        ("" for o in service_options if o.code == "EPRAIndicator"), None
                    ),
                )
                if len(service_options) > 0
                else None,
                ShipmentRatingOptions=PRate.ShipmentRatingOptionsType(
                    NegotiatedRatesIndicator="" if is_negotiated_rate else None,
                    FRSShipmentIndicator=""
                    if any([o.code == "FRSShipmentIndicator" for o in rating_options])
                    else None,
                    RateChartIndicator=""
                    if any([o.code == "RateChartIndicator" for o in rating_options])
                    else None,
                    UserLevelDiscountIndicator=""
                    if (
                        any(
                            [
                                o.code == "UserLevelDiscountIndicator"
                                for o in rating_options
                            ]
                        )
                        and is_negotiated_rate
                    )
                    else None,
                )
                if len(rating_options) > 0 or is_negotiated_rate
                else None,
                InvoiceLineTotal=None,
                RatingMethodRequestedIndicator=None,
                TaxInformationIndicator=None,
                PromotionalDiscountInformation=None,
                DeliveryTimeInformation=None,
            ),
        )
