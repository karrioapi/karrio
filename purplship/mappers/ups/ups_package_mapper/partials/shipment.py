from pyups import package_ship as PShip, common as Common
from lxml import etree
from .interface import T, UPSMapperBase
from purplship.domain.Types.units import DimensionUnit
from purplship.mappers.ups.ups_units import (
    ShippingPackagingType,
    ShippingServiceCode,
    WeightUnit,
)


class UPSMapperPartial(UPSMapperBase):

    def parse_package_shipment_response(
        self, shipmentNode: etree.ElementBase
    ) -> T.ShipmentDetails:
        shipmentResponse = PShip.ShipmentResponse()
        shipmentResponse.build(shipmentNode)
        shipment = shipmentResponse.ShipmentResults

        if not shipment.NegotiatedRateCharges:
            total_charge = (
                shipment.ShipmentCharges.TotalChargesWithTaxes
                or shipment.ShipmentCharges.TotalCharges
            )
        else:
            total_charge = (
                shipment.NegotiatedRateCharges.TotalChargesWithTaxes
                or shipment.NegotiatedRateCharges.TotalCharge
            )

        return T.ShipmentDetails(
            carrier=self.client.carrier_name,
            tracking_numbers=[pkg.TrackingNumber for pkg in shipment.PackageResults],
            total_charge=T.ChargeDetails(
                name="Shipment charge",
                amount=total_charge.MonetaryValue,
                currency=total_charge.CurrencyCode,
            ),
            charges=[
                T.ChargeDetails(
                    name=charge.Code,
                    amount=charge.MonetaryValue,
                    currency=charge.CurrencyCode,
                )
                for charge in [
                    shipment.ShipmentCharges.TransportationCharges,
                    shipment.ShipmentCharges.ServiceOptionsCharges,
                    shipment.ShipmentCharges.BaseServiceCharge,
                ]
                if charge is not None
            ],
            documents=[
                pkg.ShippingLabel.GraphicImage
                for pkg in (shipment.PackageResults or [])
            ],
            reference=T.ReferenceDetails(
                value=shipmentResponse.Response.TransactionReference.CustomerContext,
                type="CustomerContext",
            ),
        )

    def create_package_ship_request(
        self, payload: T.ShipmentRequest
    ) -> PShip.ShipmentRequest:
        services = [
            ShippingServiceCode[svc]
            for svc in payload.shipment.services
            if svc in ShippingServiceCode.__members__
        ]
        return PShip.ShipmentRequest(
            Request=Common.RequestType(
                RequestOption=payload.shipment.extra.get("RequestOption")
                or ["validate"],
                SubVersion=None,
                TransactionReference=Common.TransactionReferenceType(
                    CustomerContext=", ".join(payload.shipment.references),
                    TransactionIdentifier=payload.shipment.extra.get(
                        "TransactionIdentifier"
                    ),
                ),
            ),
            Shipment=PShip.ShipmentType(
                Description=payload.shipment.extra.get("Description"),
                ReturnService=None,
                DocumentsOnlyIndicator="" if payload.shipment.is_document else None,
                Shipper=PShip.ShipperType(
                    Name=payload.shipper.company_name,
                    AttentionName=payload.shipper.person_name,
                    CompanyDisplayableName=payload.shipper.extra.get(
                        "CompanyDisplayableName"
                    ),
                    TaxIdentificationNumber=payload.shipper.tax_id,
                    TaxIDType=None,
                    Phone=PShip.ShipPhoneType(
                        Number=payload.shipper.phone_number,
                        Extension=payload.shipper.extra.get("Extension"),
                    )
                    if payload.shipper.phone_number is not None
                    else None,
                    ShipperNumber=payload.shipper.account_number,
                    FaxNumber=payload.shipper.extra.get("FaxNumber"),
                    EMailAddress=payload.shipper.email_address,
                    Address=PShip.ShipAddressType(
                        AddressLine=payload.shipper.address_lines,
                        City=payload.shipper.city,
                        StateProvinceCode=payload.shipper.state_code,
                        PostalCode=payload.shipper.postal_code,
                        CountryCode=payload.shipper.country_code,
                    ),
                ),
                ShipTo=PShip.ShipToType(
                    Name=payload.recipient.company_name,
                    AttentionName=payload.recipient.person_name,
                    CompanyDisplayableName=payload.recipient.extra.get(
                        "CompanyDisplayableName"
                    ),
                    TaxIdentificationNumber=payload.recipient.tax_id,
                    TaxIDType=None,
                    Phone=PShip.ShipPhoneType(
                        Number=payload.recipient.phone_number,
                        Extension=payload.recipient.extra.get("Extension"),
                    )
                    if payload.recipient.phone_number is not None
                    else None,
                    FaxNumber=payload.recipient.extra.get("FaxNumber"),
                    EMailAddress=payload.recipient.email_address,
                    Address=PShip.ShipAddressType(
                        AddressLine=payload.recipient.address_lines,
                        City=payload.recipient.city,
                        StateProvinceCode=payload.recipient.state_code,
                        PostalCode=payload.recipient.postal_code,
                        CountryCode=payload.recipient.country_code,
                    ),
                    LocationID=None,
                ),
                AlternateDeliveryAddress=(
                    lambda alternate: PShip.AlternateDeliveryAddressType(
                        Name=alternate.company_name,
                        AttentionName=alternate.person_name,
                        UPSAccessPointID=alternate.extra.get("UPSAccessPointID"),
                        Address=PShip.ShipAddressType(
                            AddressLine=alternate.address_lines,
                            City=alternate.city,
                            StateProvinceCode=alternate.state_code,
                            PostalCode=alternate.postal_code,
                            CountryCode=alternate.country_code,
                        ),
                    )
                )(T.Party(payload.shipment.extra.get("AlternateDeliveryAddress")))
                if "AlternateDeliveryAddress" in payload.shipment.extra
                else None,
                ShipFrom=(
                    lambda shipFrom: PShip.ShipFromType(
                        Name=shipFrom.company_name,
                        AttentionName=shipFrom.person_name,
                        CompanyDisplayableName=shipFrom.extra.get(
                            "CompanyDisplayableName"
                        ),
                        TaxIdentificationNumber=shipFrom.tax_id,
                        TaxIDType=None,
                        Phone=PShip.ShipPhoneType(
                            Number=shipFrom.phone_number,
                            Extension=shipFrom.extra.get("Extension"),
                        )
                        if shipFrom.phone_number is not None
                        else None,
                        FaxNumber=shipFrom.extra.get("FaxNumber"),
                        EMailAddress=shipFrom.email_address,
                        Address=PShip.ShipAddressType(
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
                PaymentInformation=PShip.PaymentInfoType(
                    ShipmentCharge=[
                        PShip.ShipmentChargeType(
                            Type=payload.shipment.extra.get("ShipmentCharge").get(
                                "Type"
                            )
                            if "ShipmentCharge" in payload.shipment.extra
                            else None,
                            BillShipper=PShip.BillShipperType(
                                AccountNumber=payload.shipment.payment_account_number
                                or payload.shipper.account_number,
                                CreditCard=(
                                    lambda card: PShip.CreditCardType(
                                        Type=card.get("Type"),
                                        Number=card.get("Number"),
                                        ExpirationDate=card.get("ExpirationDate"),
                                        SecurityCode=card.get("Type"),
                                        Address=(
                                            lambda address: PShip.ShipAddressType(
                                                AddressLine=address.address_lines,
                                                City=address.city,
                                                StateProvinceCode=address.state_code,
                                                PostalCode=address.postal_code,
                                                CountryCode=address.country_code,
                                            )
                                        )(T.Party(**card.get("Address")))
                                        if "Address" in card
                                        else None,
                                    )
                                )(payload.shipment.extra.get("CreditCard"))
                                if "CreditCard" in payload.shipment.extra
                                else None,
                                AlternatePaymentMethod=payload.shipment.payment_type,
                            )
                            if payload.shipment.paid_by == "SENDER"
                            else None,
                            BillReceiver=PShip.BillReceiverType(
                                AccountNumber=payload.recipient.account_number,
                                Address=PShip.BillReceiverAddressType(
                                    PostalCode=payload.recipient.postal_code
                                ),
                            )
                            if not payload.shipment.paid_by
                            else None,
                            BillThirdParty=PShip.BillThirdPartyChargeType(
                                AccountNumber=payload.shipment.payment_account_number,
                                Address=PShip.BillReceiverAddressType(
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
                ),
                FRSPaymentInformation=None,
                FreightShipmentInformation=None,
                GoodsNotInFreeCirculationIndicator=None,
                ShipmentRatingOptions=None,
                MovementReferenceNumber=None,
                ReferenceNumber=None,
                Service=PShip.ServiceType(Code=services[0].value)
                if len(services) > 0
                else None,
                InvoiceLineTotal=None,
                NumOfPiecesInShipment=payload.shipment.total_items,
                USPSEndorsement=None,
                MILabelCN22Indicator=None,
                SubClassification=None,
                CostCenter=None,
                PackageID=None,
                IrregularIndicator=None,
                ShipmentIndicationType=None,
                MIDualReturnShipmentKey=None,
                MIDualReturnShipmentIndicator=None,
                RatingMethodRequestedIndicator=None,
                TaxInformationIndicator=None,
                PromotionalDiscountInformation=None,
                ShipmentServiceOptions=None,
                Package=[
                    PShip.PackageType(
                        Description=pkg.description,
                        Packaging=PShip.PackagingType(
                            Code=ShippingPackagingType[pkg.packaging_type].value,
                            Description=None,
                        )
                        if pkg.packaging_type != None
                        else None,
                        Dimensions=PShip.DimensionsType(
                            UnitOfMeasurement=PShip.ShipUnitOfMeasurementType(
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
                        PackageWeight=PShip.PackageWeightType(
                            UnitOfMeasurement=PShip.ShipUnitOfMeasurementType(
                                Code=WeightUnit[payload.shipment.weight_unit].value,
                                Description=None,
                            ),
                            Weight=pkg.weight,
                        ),
                        LargePackageIndicator=pkg.extra.get("LargePackageIndicator"),
                        ReferenceNumber=None,
                        AdditionalHandlingIndicator=None,
                        PackageServiceOptions=None,
                        Commodity=None,
                        HazMatPackageInformation=None,
                    )
                    for pkg in payload.shipment.items
                ],
            ),
            LabelSpecification=PShip.LabelSpecificationType(
                LabelImageFormat=PShip.LabelImageFormatType(
                    Code=payload.shipment.label.format,
                    Description=payload.shipment.label.format,
                ),
                HTTPUserAgent=payload.shipment.label.extra.get("HTTPUserAgent"),
                LabelStockSize=None,
                Instruction=payload.shipment.label.extra.get("Instruction"),
            )
            if payload.shipment.label is not None
            else None,
            ReceiptSpecification=None,
        )
