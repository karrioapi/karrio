import time
from pydhl.datatypes_global_v61 import MetaData
from pydhl import (
    DCT_req_global as Req,
    DCT_Response_global as Res,
    datatypes_global_v61 as GType,
    DCTRequestdatatypes_global as ReqType
)
from purplship.mappers.dhl.dhl_units import (
    ProductCode, 
    ServiceCode
)
from purplship.domain.Types.units import (
    Currency,
    Country
)
from .interface import (
    reduce, Tuple, List, T, 
    DHLMapperBase
)


class DHLMapperPartial(DHLMapperBase):
    
    def parse_dct_response(self, response: 'XMLElement') -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        qtdshp_list = response.xpath(
            './/*[local-name() = $name]', name="QtdShp")
        quotes = reduce(self._extract_quote, qtdshp_list, [])
        return (quotes, self.parse_error_response(response))

    def _extract_quote(self, quotes: List[T.QuoteDetails], qtdshpNode: 'XMLElement') -> List[T.QuoteDetails]:
        qtdshp = Res.QtdShpType()
        qtdshp.build(qtdshpNode)
        ExtraCharges = list(map(lambda s: T.ChargeDetails(
            name=s.LocalServiceTypeName, amount=float(s.ChargeValue or 0)), qtdshp.QtdShpExChrg))
        Discount_ = reduce(
            lambda d, ec: d + ec.value if "Discount" in ec.name else d, ExtraCharges, 0)
        DutiesAndTaxes_ = reduce(
            lambda d, ec: d + ec.value if "TAXES PAID" in ec.name else d, ExtraCharges, 0)
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
                extra_charges=list(map(lambda s: T.ChargeDetails(
                    name=s.LocalServiceTypeName, amount=float(s.ChargeValue or 0)), qtdshp.QtdShpExChrg))
            )
        ]

    def create_dct_request(self, payload: T.shipment_request) -> Req.DCTRequest:
        is_dutiable = payload.shipment.declared_value != None
        extra_services = (
            [ServiceCode[svc] for svc in payload.shipment.extra_services if svc in ServiceCode.__members__] +
            ([] if not payload.shipment.insured_amount else [ServiceCode.Shipment_Insurance]) +
            ([] if not is_dutiable or "Duties_and_Taxes_Paid" in payload.shipment.extra_services else [ServiceCode.Duties_and_Taxes_Paid])
        )

        if payload.shipment.service_type != None:
            service_type = ProductCode[payload.shipment.service_type]
        elif payload.shipment.is_document:
            service_type = ProductCode.EXPRESS_WORLDWIDE_DOC
        else:
            service_type = ProductCode.EXPRESS_WORLDWIDE_P

        default_packaging_type = "FLY" if payload.shipment.is_document else "BOX"

        GetQuote = Req.GetQuoteType(
            Request=self.init_request(), 
            From=Req.DCTFrom(
                CountryCode=payload.shipper.country_code,
                Postalcode=payload.shipper.postal_code,
                City=payload.shipper.city,
                Suburb=payload.shipper.state_code
            ), 
            To=Req.DCTTo(
                CountryCode=payload.recipient.country_code,
                Postalcode=payload.recipient.postal_code,
                City=payload.recipient.city,
                Suburb=payload.recipient.state_code
            ), 
            BkgDetails=ReqType.BkgDetailsType(
                PaymentCountryCode=payload.shipment.payment_country_code or "CA",
                NetworkTypeCode=None,
                WeightUnit=payload.shipment.weight_unit or "KG",
                DimensionUnit=payload.shipment.dimension_unit or "CM",
                ReadyTime=time.strftime("PT%HH%MM"),
                Date=time.strftime("%Y-%m-%d"),
                IsDutiable="Y" if is_dutiable else "N",
                Pieces=(lambda pieces: 
                    (
                        pieces,
                        [
                            pieces.add_Piece(ReqType.PieceType(
                                PieceID=piece.id or str(index),
                                PackageTypeCode=piece.packaging_type or default_packaging_type,
                                Height=piece.height, Width=piece.width,
                                Weight=piece.weight, Depth=piece.length
                            )) for index, piece in enumerate(payload.shipment.items)
                        ]
                    )[0]
                )(ReqType.PiecesType()),
                NumberOfPieces=payload.shipment.total_items,
                ShipmentWeight=payload.shipment.total_weight,
                Volume=payload.shipment.extra.get('Volume'),
                PaymentAccountNumber=payload.shipment.payment_account_number,
                InsuredCurrency=(payload.shipment.currency or "USD") if ServiceCode.Shipment_Insurance in extra_services else None,
                InsuredValue=payload.shipment.insured_amount,
                PaymentType=payload.shipment.payment_type,
                AcctPickupCloseTime=payload.shipment.extra.get('AcctPickupCloseTime'),
                QtdShp=[
                    ReqType.QtdShpType(
                        GlobalProductCode=service_type.value,
                        LocalProductCode=service_type.value,
                        QtdShpExChrg=[
                            ReqType.QtdShpExChrgType(
                                SpecialServiceType=svc.value,
                                LocalSpecialServiceType=None
                            ) for svc in extra_services
                        ] if len(extra_services) > 0 else None
                    )
                ]
            ),
            Dutiable=ReqType.DCTDutiable(
                DeclaredCurrency=payload.shipment.currency or "USD",
                DeclaredValue=payload.shipment.declared_value or 0
            ) if is_dutiable else None
        )
        GetQuote.Request.MetaData = MetaData(SoftwareName="3PV", SoftwareVersion="1.0")

        return Req.DCTRequest(schemaVersion="1.0", GetQuote=GetQuote)

