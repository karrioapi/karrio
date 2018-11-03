import time
from pydhl.datatypes_global_v61 import MetaData
from pydhl import (
    DCT_req_global as Req,
    DCT_Response_global as Res
)
from .interface import (
    reduce, Tuple, List, E, 
    DHLMapperBase
)


class DHLMapperPartial(DHLMapperBase):
    
    def parse_dct_response(self, response: 'XMLElement') -> Tuple[List[E.QuoteDetails], List[E.Error]]:
        qtdshp_list = response.xpath(
            './/*[local-name() = $name]', name="QtdShp")
        quotes = reduce(self._extract_quote, qtdshp_list, [])
        return (quotes, self.parse_error_response(response))

    def _extract_quote(self, quotes: List[E.QuoteDetails], qtdshpNode: 'XMLElement') -> List[E.QuoteDetails]:
        qtdshp = Res.QtdShpType()
        qtdshp.build(qtdshpNode)
        ExtraCharges = list(map(lambda s: E.ChargeDetails(
            name=s.LocalServiceTypeName, amount=float(s.ChargeValue or 0)), qtdshp.QtdShpExChrg))
        Discount_ = reduce(
            lambda d, ec: d + ec.value if "Discount" in ec.name else d, ExtraCharges, 0)
        DutiesAndTaxes_ = reduce(
            lambda d, ec: d + ec.value if "TAXES PAID" in ec.name else d, ExtraCharges, 0)
        return quotes + [
            E.QuoteDetails(
                carrier=self.client.carrier_name,
                currency=qtdshp.CurrencyCode,
                delivery_date=str(qtdshp.DeliveryDate[0].DlvyDateTime),
                pickup_date=str(qtdshp.PickupDate),
                pickup_time=str(qtdshp.PickupCutoffTime),
                service_name=qtdshp.LocalProductName,
                service_type=qtdshp.NetworkTypeCode,
                base_charge=float(qtdshp.WeightCharge or 0),
                total_charge=float(qtdshp.ShippingCharge or 0),
                duties_and_taxes=DutiesAndTaxes_,
                discount=Discount_,
                extra_charges=list(map(lambda s: E.ChargeDetails(
                    name=s.LocalServiceTypeName, amount=float(s.ChargeValue or 0)), qtdshp.QtdShpExChrg))
            )
        ]

    def create_dct_request(self, payload: E.shipment_request) -> Req.DCTRequest:
        Request_ = self.init_request()
        Request_.MetaData = MetaData(SoftwareName="3PV", SoftwareVersion="1.0")

        From_ = Req.DCTFrom(
            CountryCode=payload.shipper.country_code,
            Postalcode=payload.shipper.postal_code,
            City=payload.shipper.city,
            Suburb=payload.shipper.state_code
        )

        To_ = Req.DCTTo(
            CountryCode=payload.recipient.country_code,
            Postalcode=payload.recipient.postal_code,
            City=payload.recipient.city,
            Suburb=payload.recipient.state_code
        )

        Pieces = Req.PiecesType()
        default_packaging_type = "FLY" if payload.shipment.is_document else "BOX"
        for index, piece in enumerate(payload.shipment.items):
            Pieces.add_Piece(Req.PieceType(
                PieceID=piece.id or str(index),
                PackageTypeCode=piece.packaging_type or default_packaging_type,
                Height=piece.height, Width=piece.width,
                Weight=piece.weight, Depth=piece.length
            ))

        payment_country_code = "CA" if not payload.shipment.payment_country_code else payload.shipment.payment_country_code

        BkgDetails_ = Req.BkgDetailsType(
            PaymentCountryCode=payment_country_code,
            NetworkTypeCode=payload.shipment.extra.get('NetworkTypeCode') or "AL",
            WeightUnit=payload.shipment.weight_unit or "LB",
            DimensionUnit=payload.shipment.dimension_unit or "IN",
            ReadyTime=time.strftime("PT%HH%MM"),
            Date=time.strftime("%Y-%m-%d"),
            IsDutiable="N" if payload.shipment.is_document else "Y",
            Pieces=Pieces,
            NumberOfPieces=payload.shipment.total_items,
            ShipmentWeight=payload.shipment.total_weight,
            Volume=payload.shipment.extra.get('Volume'),
            PaymentAccountNumber=payload.shipment.payment_account_number or self.client.account_number,
            InsuredCurrency=payload.shipment.currency or "USD",
            InsuredValue=payload.shipment.insured_amount,
            PaymentType=payload.shipment.extra.get('PaymentType'),
            AcctPickupCloseTime=payload.shipment.extra.get('AcctPickupCloseTime'),
        )

        product_code = "P" if payload.shipment.is_document else "D"
        BkgDetails_.add_QtdShp(Req.QtdShpType(
            GlobalProductCode=product_code,
            LocalProductCode=product_code
        ))

        if payload.shipment.insured_amount is not None:
            BkgDetails_.QtdShp[0].add_QtdShpExChrg(
                Req.QtdShpExChrgType(SpecialServiceType="II")
            )

        if not payload.shipment.is_document:
            BkgDetails_.QtdShp[0].add_QtdShpExChrg(
                Req.QtdShpExChrgType(SpecialServiceType="DD")
            )

        GetQuote = Req.GetQuoteType(
            Request=Request_, 
            From=From_, 
            To=To_, 
            BkgDetails=BkgDetails_,
            Dutiable=Req.Dutiable(
                DeclaredValue=payload.shipment.declared_value,
                DeclaredCurrency=payload.shipment.currency,
                ScheduleB=payload.shipment.extra.get('ScheduleB'),
                ExportLicense=payload.shipment.extra.get('ExportLicense'),
                ShipperEIN=payload.shipment.extra.get('ShipperEIN'),
                ShipperIDType=payload.shipment.extra.get('ShipperIDType'),
                ConsigneeIDType=payload.shipment.extra.get('ConsigneeIDType'),
                ImportLicense=payload.shipment.extra.get('ImportLicense'),
                ConsigneeEIN=payload.shipment.extra.get('ConsigneeEIN'),
                TermsOfTrade=payload.shipment.extra.get('TermsOfTrade'),
                CommerceLicensed=payload.shipment.extra.get('CommerceLicensed'),
                Filing=(lambda filing:
                    Req.Filing(
                        FilingType=filing.get('FilingType'),
                        FTSR=filing.get('FTSR'),
                        ITN=filing.get('ITN'),
                        AES4EIN=filing.get('AES4EIN')
                    )
                )(payload.shipment.extra.get('Filing')) if 'Filing' in payload.shipment.extra else None
            ) if payload.shipment.declared_value is not None else None
        )

        return Req.DCTRequest(schemaVersion="1.0", GetQuote=GetQuote)

