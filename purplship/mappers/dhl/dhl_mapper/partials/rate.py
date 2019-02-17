import time
from lxml import etree
from pydhl.datatypes_global_v61 import MetaData
from pydhl import (
    DCT_req_global as Req,
    DCT_Response_global as Res,
    datatypes_global_v61 as GType,
    DCTRequestdatatypes_global as ReqType,
)
from purplship.mappers.dhl.dhl_units import Product, Service, DCTPackageType
from purplship.domain.Types.units import DimensionUnit, WeightUnit
from .interface import reduce, Tuple, List, T, DHLMapperBase


class DHLMapperPartial(DHLMapperBase):
    def parse_dct_response(
        self, response: etree.ElementBase
    ) -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        qtdshp_list = response.xpath(".//*[local-name() = $name]", name="QtdShp")
        quotes: List[T.QuoteDetails] = reduce(self._extract_quote, qtdshp_list, [])
        return (quotes, self.parse_error_response(response))

    def _extract_quote(
        self, quotes: List[T.QuoteDetails], qtdshpNode: etree.ElementBase
    ) -> List[T.QuoteDetails]:
        qtdshp = Res.QtdShpType()
        qtdshp.build(qtdshpNode)
        ExtraCharges = list(
            map(
                lambda s: T.ChargeDetails(
                    name=s.LocalServiceTypeName, amount=float(s.ChargeValue or 0)
                ),
                qtdshp.QtdShpExChrg,
            )
        )
        Discount_ = reduce(
            lambda d, ec: d + ec.amount if "Discount" in ec.name else d,
            ExtraCharges,
            0.0,
        )
        DutiesAndTaxes_ = reduce(
            lambda d, ec: d + ec.amount if "TAXES PAID" in ec.name else d,
            ExtraCharges,
            0.0,
        )
        return quotes + [
            T.QuoteDetails(
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
                extra_charges=list(
                    map(
                        lambda s: T.ChargeDetails(
                            name=s.LocalServiceTypeName,
                            amount=float(s.ChargeValue or 0),
                        ),
                        qtdshp.QtdShpExChrg,
                    )
                ),
            )
        ]

    def create_dct_request(self, payload: T.shipment_request) -> Req.DCTRequest:
        default_product_code = (
            Product.EXPRESS_WORLDWIDE_DOC
            if payload.shipment.is_document
            else Product.EXPRESS_WORLDWIDE
        )
        products = [
            Product[svc]
            for svc in payload.shipment.services
            if svc in Product.__members__
        ] + [default_product_code]
        is_dutiable = payload.shipment.declared_value != None
        default_packaging_type = (
            DCTPackageType.SM if payload.shipment.is_document else DCTPackageType.BOX
        )
        options = (
            [
                Service[svc.code]
                for svc in payload.shipment.options
                if svc.code in Service.__members__
            ]
            + (
                []
                if not payload.shipment.insured_amount
                or "Shipment_Insurance" in [o.code for o in payload.shipment.options]
                else [Service.Shipment_Insurance]
            )
            + (
                []
                if not is_dutiable
                or "Duties_and_Taxes_Paid" in [o.code for o in payload.shipment.options]
                else [Service.Duties_and_Taxes_Paid]
            )
        )

        GetQuote = Req.GetQuoteType(
            Request=self.init_request(),
            From=Req.DCTFrom(
                CountryCode=payload.shipper.country_code,
                Postalcode=payload.shipper.postal_code,
                City=payload.shipper.city,
                Suburb=payload.shipper.state_code,
            ),
            To=Req.DCTTo(
                CountryCode=payload.recipient.country_code,
                Postalcode=payload.recipient.postal_code,
                City=payload.recipient.city,
                Suburb=payload.recipient.state_code,
            ),
            BkgDetails=ReqType.BkgDetailsType(
                PaymentCountryCode=payload.shipment.payment_country_code or "CA",
                NetworkTypeCode=payload.shipment.extra.get("NetworkTypeCode"),
                WeightUnit=WeightUnit[payload.shipment.weight_unit or "KG"].value,
                DimensionUnit=DimensionUnit[
                    payload.shipment.dimension_unit or "CM"
                ].value,
                ReadyTime=time.strftime("PT%HH%MM"),
                Date=time.strftime("%Y-%m-%d"),
                IsDutiable="Y" if is_dutiable else "N",
                Pieces=ReqType.PiecesType(
                    Piece=[
                        ReqType.PieceType(
                            PieceID=piece.id or str(index),
                            PackageTypeCode=(
                                DCTPackageType[piece.packaging_type]
                                if piece.packaging_type != None
                                else default_packaging_type
                            ).value,
                            Height=piece.height,
                            Width=piece.width,
                            Weight=piece.weight,
                            Depth=piece.length,
                        )
                        for index, piece in enumerate(payload.shipment.items)
                    ]
                ),
                NumberOfPieces=payload.shipment.total_items,
                ShipmentWeight=payload.shipment.total_weight,
                Volume=payload.shipment.extra.get("Volume"),
                PaymentAccountNumber=payload.shipment.payment_account_number,
                InsuredCurrency=(payload.shipment.currency or "USD")
                if Service.Shipment_Insurance in options
                else None,
                InsuredValue=payload.shipment.insured_amount,
                PaymentType=payload.shipment.payment_type,
                AcctPickupCloseTime=payload.shipment.extra.get("AcctPickupCloseTime"),
                QtdShp=[
                    ReqType.QtdShpType(
                        GlobalProductCode=product.value,
                        LocalProductCode=product.value,
                        QtdShpExChrg=[
                            ReqType.QtdShpExChrgType(
                                SpecialServiceType=svc.value,
                                LocalSpecialServiceType=None,
                            )
                            for svc in options
                        ]
                        if len(options) > 0
                        else None,
                    )
                    for product in products
                ],
            ),
            Dutiable=ReqType.DCTDutiable(
                DeclaredCurrency=payload.shipment.currency or "USD",
                DeclaredValue=payload.shipment.declared_value or 0,
            )
            if is_dutiable
            else None,
        )
        GetQuote.Request.MetaData = MetaData(SoftwareName="3PV", SoftwareVersion="1.0")

        return Req.DCTRequest(schemaVersion="1.0", GetQuote=GetQuote)
